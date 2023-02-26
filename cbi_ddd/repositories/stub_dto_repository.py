from typing import Type, List

from ulid import ULID

from cbi_ddd.interfaces import (
    DTORepository,
    DTOModel,
    errors,
)
from cbi_ddd.helpers import DateTimeHelper


class StubDTORepository(DTORepository):
    data = {}

    @classmethod
    def init_table(cls, tablename, **extra):
        init_error = extra.get('init_error', False)
        if init_error:
            raise errors.InitStorageError()

        if tablename not in cls.data:
            cls.data[tablename] = []

    @classmethod
    def is_exists(cls, tablename: str, object_id: str) -> bool:
        cls.init_table(tablename)
        for item in cls.data[tablename]:
            if item.object_id == object_id:
                return True

        return False
    
    @classmethod
    def remove_item(cls, tablename: str, object_id: str) -> bool:
        cls.init_table(tablename)
        if cls.is_exists(tablename, object_id):
            items = cls.data[tablename]
            cls.data[tablename] = [item for item in items if item.object_id != object_id]
            return True
        return False

    @classmethod
    def save(cls, model: DTOModel, **extra) -> DTOModel:
        save_error = extra.get('save_error', False)
        cls.init_table(model.opts.tablename, **extra)

        if save_error:
            raise errors.StubSaveError()

        model.updated = DateTimeHelper.utcnow()

        if not model.object_id:
            model.object_id = str(ULID().to_uuid())
            model.created = DateTimeHelper.utcnow()

        if cls.is_exists(model.opts.tablename, model.object_id):
            cls.remove_item(model.opts.tablename, model.object_id)

        cls.data[model.opts.tablename].append(model)

        return model
    
    @classmethod
    def find(cls, model_cls: Type[DTOModel], conditions: dict, offset: int, limit: int, **extra) -> List[DTOModel]:
        find_error = extra.get('find_error', False)
        cls.init_table(model_cls.opts.tablename, **extra)

        items = []

        if find_error:
            raise errors.StubFindError()

        cond_list = [(k, v) for k, v in conditions.items()]
        for item in cls.data[model_cls.opts.tablename]:
            result = True
            for cond in cond_list:
                if not hasattr(item, cond[0]):
                    result = False
                else:
                    if getattr(item, cond[0]) != cond[1]:
                        result = False

            if result:
                items.append(item)

        return items[offset:offset+limit]

    @classmethod
    def delete(cls, model_cls: Type[DTOModel], object_id: str, **extra) -> bool:
        delete_error = extra.get('delete_error', False)
        cls.init_table(model_cls.opts.tablename, **extra)

        if delete_error:
            raise errors.StubDeleteError()

        return cls.remove_item(model_cls.opts.tablename, object_id)
