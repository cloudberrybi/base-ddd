from typing import List, Type

from cbi_ddd.interfaces import (
    DataModel,
    DTOModel,
    DTORepository,
    Error,
)


class StorageRepository:
    @classmethod
    def save(cls, data: DataModel) -> DataModel | Error:
        try:
            dto_model_cls: Type[DTOModel] = data._opts.DTO.model
            dto_repository: Type[DTORepository] = data._opts.DTO.model.opts.repository

            dto_object: DTOModel = dto_model_cls.from_data_model(data)
            dto_object = dto_repository.save(dto_object)

            return dto_object.to_data_model()
        except Error as err:
            return err

    @classmethod
    def get(cls, model: Type[DataModel], conditions: dict) -> DataModel | None | Error:
        result: List[DataModel] | Error = cls.find(
            model=model,
            conditions=conditions,
            offset=0,
            limit=1,
        )

        if isinstance(result, Error):
            return result

        return result[0] if len(result) > 0 else None
    
    @classmethod
    def find(cls, model: Type[DataModel], conditions: dict, offset: int, limit: int) -> List[DataModel] | Error:
        try:
            dto_model_cls: Type[DTOModel] = model._opts.DTO.model
            dto_repository: Type[DTORepository] = model._opts.DTO.model.opts.repository

            result: List[DTOModel] = dto_repository.find(
                dto_model_cls,
                conditions,
                offset,
                limit,
            )
            
            return [result_item.to_data_model() for result_item in result]
        except Error as err:
            return err
    
    @classmethod
    def delete(cls, model: Type[DataModel], conditions: dict, limit: int = 1) -> dict | Error:
        try:
            dto_model_cls: Type[DTOModel] = model._opts.DTO.model
            dto_repository: Type[DTORepository] = model._opts.DTO.model.opts.repository

            result = {
                'count': 0,
                'ids': [],
            }

            result: List[DTOModel] = dto_repository.find(
                dto_model_cls,
                conditions,
                0,
                limit,
            )

            for result_item in result:
                ok = dto_repository.delete(
                    dto_model_cls,
                    result_item.object_id,
                )

                if ok:
                    result['count'] += 1
                    result['ids'].append(result_item.object_id)

            return result
        except Error as err:
            return err
