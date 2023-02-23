from typing import List, Type

from dramatiq import Actor

from cbi_ddd.interfaces import DataModel


class DataModelRepository:
    save_task: Actor
    find_task: Actor
    delete_task: Actor

    @classmethod
    def save(cls, **kwargs) -> DataModel:
        return cls.save_task.send(**kwargs).get_result(block=True)
    
    @classmethod
    def usave(cls, **kwargs) -> None:
        return cls.save_task.send(**kwargs)

    @classmethod
    def get(cls, conditions: dict) -> DataModel | None:
        result = cls.find_task.send(conditions=conditions, offset=0, limit=1).get_result(block=True)

        return result[0] if len(result) > 0 else None
    
    @classmethod
    def find(cls, conditions: dict, offset: int, limit: int) -> List[DataModel]:
        return cls.find_task.send(conditions=conditions, offset=offset, limit=limit).get_result(block=True)
    
    @classmethod
    def delete(cls, object_id: str) -> bool:
        return cls.delete_task.send(object_id=object_id).get_result(block=True)
    
    @classmethod
    def udelete(cls, object_id: str) -> None:
        return cls.delete_task.send(object_id=object_id)
