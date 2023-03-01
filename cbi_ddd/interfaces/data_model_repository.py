import dramatiq

from typing import List, Type, Tuple

from dramatiq import Actor

from cbi_ddd.helpers.rabbitmq import RabbitMQHelper

from .data_model import DataModel
from .errors import Error


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
    def create_save_actors(cls):
        blocking_queue_name = f'{cls.repository_id}_save'
        unblocking_queue_name = f'{cls.repository_id}_usave'

        def save_handler(extra:dict={}, **data) -> DataModel | Error:
            from cbi_ddd.repositories.storage_repository import StorageRepository

            model_data = cls.model(**data)
            model_data = cls.pre_save(model_data)

            save_result = StorageRepository.save(model_data, **extra)
            if isinstance(save_result, Error):
                save_result = cls.post_save_error(model_data, save_result)
            else:
                save_result = cls.post_save_success(save_result)
            return save_result

        def blocking_actor(extra:dict={}, **data) -> DataModel | Error:
            return save_handler(extra=extra, **data)
        
        def unblocking_actor(extra:dict={}, **data):
            save_handler(extra=extra, **data)

        cls.save_actor = dramatiq.actor(
            store_results=True,
            queue_name=RabbitMQHelper.queue_name(blocking_queue_name),
            actor_name=blocking_queue_name,
        )(blocking_actor)

        cls.usave_actor = dramatiq.actor(
            store_results=False,
            queue_name=RabbitMQHelper.queue_name(unblocking_queue_name),
            actor_name=unblocking_queue_name
        )(unblocking_actor)

    @classmethod
    def create_get_actor(cls):
        queue_name = f'{cls.repository_id}_get'

        def actor(conditions: dict, **extra) -> DataModel | None | Error:
            from cbi_ddd.repositories.storage_repository import StorageRepository

            conditions = cls.pre_get(conditions)

            get_result = StorageRepository.get(cls.model, conditions, **extra)
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

    @classmethod
    def create_find_actor(cls):
        queue_name = f'{cls.repository_id}_find'

        def actor(conditions: dict, offset: int, limit: int, **extra) -> List[DataModel] | Error:
            from cbi_ddd.repositories.storage_repository import StorageRepository

            conditions, offset, limit = cls.pre_find(conditions, offset, limit)

            find_result = StorageRepository.find(cls.model, conditions, offset, limit, **extra)
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

    @classmethod
    def create_delete_actors(cls):
        blocking_queue_name = f'{cls.repository_id}_delete'
        unblocking_queue_name = f'{cls.repository_id}_udelete'

        def actor(conditions: dict, limit: int, **extra) -> dict | Error:
            from cbi_ddd.repositories.storage_repository import StorageRepository

            conditions, limit = cls.pre_delete(conditions, limit)

            delete_result = StorageRepository.delete(cls.model, conditions, limit, **extra)
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

    @classmethod
    def init_actors(cls, save=True, get=True, find=True, delete=True):
        if save:
            cls.create_save_actors()

        if get:
            cls.create_get_actor()

        if find:
            cls.create_find_actor()

        if delete:
            cls.create_delete_actors()

    @classmethod
    def save(cls, extra={}, **kwargs) -> DataModel | Error:
        return cls.save_actor.send(extra=extra, **kwargs).get_result(block=True)
    
    @classmethod
    def usave(cls, extra={}, **kwargs) -> None:
        return cls.usave_actor.send(extra=extra, **kwargs)

    @classmethod
    def get(cls, conditions: dict, **extra) -> DataModel | None | Error:
        return cls.get_actor.send(conditions=conditions, **extra).get_result(block=True)

    @classmethod
    def find(cls, conditions: dict, offset: int, limit: int, **extra) -> List[DataModel] | Error:
        return cls.find_actor.send(conditions=conditions, offset=offset, limit=limit, **extra).get_result(block=True)

    @classmethod
    def delete(cls, conditions: dict, limit: int = 1, **extra) -> bool | Error:
        return cls.delete_actor.send(conditions=conditions, limit=limit, **extra).get_result(block=True)

    @classmethod
    def udelete(cls, conditions: dict, limit: int = 1, **extra) -> None:
        return cls.udelete_actor.send(conditions=conditions, limit=limit, **extra)
