import dramatiq

from typing import List, Type, Tuple

from dramatiq import Actor

from cbi_ddd.interfaces import (
    DataModel,
    Error,
)
from cbi_ddd.helpers import RabbitMQHelper

from .storage_repository import StorageRepository


class DataModelRepository:
    repository_id = 'default_repository'
    model: Type[DataModel]

    save_actor: Actor
    usave_actor: Actor
    get_actor: Actor
    find_actor: Actor
    delete_actor: Actor
    udelete_actor: Actor

    @classmethod
    def pre_save(cls, data: DataModel) -> DataModel:
        return data

    @classmethod
    def post_save_success(cls, data: DataModel) -> DataModel:
        return data

    @classmethod
    def post_save_error(cls, data: DataModel, err: Error) -> Error:
        return err

    @classmethod
    def pre_get(cls, conditions: dict) -> dict:
        return conditions

    @classmethod
    def post_get_success(cls, conditions: dict, data: DataModel | None) -> DataModel | None:
        return data

    @classmethod
    def post_get_error(cls, conditions: dict, err: Error) -> Error:
        return err

    @classmethod
    def pre_find(cls, conditions: dict, offset: int, limit: int) -> Tuple[dict, int, int]:
        return (conditions, offset, limit)
    
    @classmethod
    def post_find_success(cls, conditions: dict, offset: int, limit: int, data: List[DataModel]) -> List[DataModel]:
        return data
    
    @classmethod
    def post_find_error(cls, conditions: dict, offset: int, limit: int, err: Error) -> Error:
        return err
    
    @classmethod
    def pre_delete(cls, conditions: dict, limit: int) -> Tuple[dict, int]:
        return (conditions, limit)
    
    @classmethod
    def post_delete_success(cls, conditions: dict, limit: int, data: dict) -> dict:
        return data
    
    @classmethod
    def post_delete_error(cls, conditions: dict, limit: int, err: Error) -> Error:
        return err

    @classmethod
    def create_save_actors(cls) -> Tuple[Actor, Actor]:
        blocking_queue_name = f'{cls.repository_id}_save'
        unblocking_queue_name = f'{cls.repository_id}_usave'

        def actor(**data) -> DataModel | Error:
            model_data = cls.model(**data)
            model_data = cls.pre_save(model_data)

            save_result = StorageRepository.save(model_data)
            if isinstance(save_result, Error):
                save_result = cls.post_save_error(model_data, save_result)
            else:
                save_result = cls.post_save_success(save_result)
            return save_result

        cls.save_actor = dramatiq.actor(
            store_results=True,
            queue_name=RabbitMQHelper.queue_name(blocking_queue_name),
            actor_name=blocking_queue_name,
        )(actor)

        cls.usave_actor = dramatiq.actor(
            store_results=False,
            queue_name=RabbitMQHelper.queue_name(unblocking_queue_name),
            actor_name=unblocking_queue_name
        )(actor)

        return (cls.save_actor, cls.usave_actor)

    @classmethod
    def create_get_actor(cls) -> Actor:
        queue_name = f'{cls.repository_id}_get'

        def actor(conditions: dict) -> DataModel | None | Error:
            conditions = cls.pre_get(conditions)

            get_result = StorageRepository.get(cls.model, conditions)
            if isinstance(get_result, Error):
                get_result = cls.post_get_error(conditions, get_result)
            else:
                get_result = cls.post_get_success(conditions, get_result)
            return get_result
        
        cls.get_actor = dramatiq.actor(
            store_results=True,
            queue_name=RabbitMQHelper.queue_name(queue_name),
            actor_name=queue_name,
        )(actor)

        return cls.get_actor

    @classmethod
    def create_find_actor(cls) -> Actor:
        queue_name = f'{cls.repository_id}_find'

        def actor(conditions: dict, offset: int, limit: int) -> List[DataModel] | Error:
            conditions, offset, limit = cls.pre_find(conditions, offset, limit)

            find_result = StorageRepository.find(cls.model, conditions, offset, limit)
            if isinstance(find_result, Error):
                find_result = cls.post_find_error(conditions, offset, limit, find_result)
            else:
                find_result = cls.post_find_success(conditions, offset, limit, find_result)
            return find_result

        cls.find_actor = dramatiq.actor(
            store_results=True,
            queue_name=RabbitMQHelper.queue_name(queue_name),
            actor_name=queue_name,
        )(actor)

        return cls.find_actor

    @classmethod
    def create_delete_actors(cls) -> Actor:
        blocking_queue_name = f'{cls.repository_id}_delete'
        unblocking_queue_name = f'{cls.repository_id}_udelete'

        def actor(conditions: dict, limit: int) -> dict | Error:
            conditions, limit = cls.pre_delete(conditions, limit)

            delete_result = StorageRepository.delete(cls.model, conditions, limit)
            if isinstance(delete_result, Error):
                delete_result = cls.post_delete_error(conditions, limit, delete_result)
            else:
                delete_result = cls.post_delete_success(conditions, limit, delete_result)
            return delete_result
        
        cls.delete_actor = dramatiq.actor(
            store_results=True,
            queue_name=RabbitMQHelper.queue_name(blocking_queue_name),
            actor_name=blocking_queue_name,
        )(actor)

        cls.udelete_actor = dramatiq.actor(
            store_results=False,
            queue_name=RabbitMQHelper.queue_name(unblocking_queue_name),
            actor_name=unblocking_queue_name
        )(actor)

        return (cls.delete_actor, cls.udelete_actor)

    @classmethod
    def save(cls, **kwargs) -> DataModel:
        return cls.save_actor.send(**kwargs).get_result(block=True)
    
    @classmethod
    def usave(cls, **kwargs) -> None:
        return cls.usave_actor.send(**kwargs)

    @classmethod
    def get(cls, conditions: dict) -> DataModel | None:
        return cls.get_actor.send(conditions=conditions).get_result(block=True)

    @classmethod
    def find(cls, conditions: dict, offset: int, limit: int) -> List[DataModel]:
        return cls.find_actor.send(conditions=conditions, offset=offset, limit=limit).get_result(block=True)

    @classmethod
    def delete(cls, object_id: str) -> bool:
        return cls.delete_actor.send(object_id=object_id).get_result(block=True)

    @classmethod
    def udelete(cls, object_id: str) -> None:
        return cls.udelete_actor.send(object_id=object_id)
