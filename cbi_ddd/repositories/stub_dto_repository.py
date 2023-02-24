from typing import Type, List

from cbi_ddd.interfaces import (
    DTORepository,
    DTOModel,
    Error,
)


class StubError(Error):
    pass


class StubDTORepository(DTORepository):
    data = {}

    save_error: bool = False
    find_error: bool = False
    delete_error: bool = False

    @classmethod
    def init_table(cls, tablename):
        if tablename not in cls.data:
            cls.data[tablename] = []

    @classmethod
    def is_exists(cls, tablename, object_id) -> bool:
        for item in cls.data[tablename]:
            if item.object_id == object_id:
                return True

        return False
    
    @classmethod
    def remove_item(cls, tablename: str, object_id: str) -> bool:
        if cls.is_exists(tablename, object_id):
            items = cls.data[tablename]
            cls.data[tablename] = [item for item in items if item.object_id != object_id]
            return True
        return False

    @classmethod
    def save(cls, model: DTOModel) -> DTOModel:
        cls.init_table(model.opts.tablename)

        if cls.save_error:
            raise StubError()

        if cls.is_exists(model.object_id):
            cls.remove_item(model.opts.tablename, model.object_id)

        cls.data[model.opts.tablename].append(model)

        return super().save(model)
    
    @classmethod
    def find(cls, model_cls: Type[DTOModel], conditions: dict, offset: int, limit: int) -> List[DTOModel]:
        cls.init_table(model_cls.opts.tablename)

        items = []

        if cls.find_error:
            raise StubError()
        
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
    def delete(cls, model_cls: Type[DTOModel], object_id: str) -> bool:
        cls.init_table(model_cls.opts.tablename)

        if cls.delete_error:
            raise StubError()

        return cls.remove_item(model_cls.opts.tablename, object_id)
