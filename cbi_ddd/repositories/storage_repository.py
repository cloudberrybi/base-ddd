from typing import List, Type

from cbi_ddd.interfaces import (
    DataModel,
    DTOModel,
    DTORepository,
    Error,
)


class StorageRepository:
    @classmethod
    def save(cls, data: DataModel, **extra) -> DataModel | Error:
        try:
            dto_model_cls: Type[DTOModel] = data._opts.DTO.model
            dto_repository: Type[DTORepository] = data._opts.DTO.model.opts.repository

            dto_object: DTOModel = dto_model_cls.from_data_model(data)
            dto_object = dto_repository.save(dto_object, **extra)

            return dto_object.to_data_model()
        except Error as err:
            return err

    @classmethod
    def get(cls, model: Type[DataModel], conditions: dict, **extra) -> DataModel | None | Error:
        result: List[DataModel] | Error = cls.find(
            model=model,
            conditions=conditions,
            offset=0,
            limit=1,
            **extra,
        )

        if isinstance(result, Error):
            return result

        return result[0] if len(result) > 0 else None
    
    @classmethod
    def find(cls, model: Type[DataModel], conditions: dict, offset: int, limit: int, **extra) -> List[DataModel] | Error:
        try:
            dto_model_cls: Type[DTOModel] = model._opts.DTO.model
            dto_repository: Type[DTORepository] = model._opts.DTO.model.opts.repository

            result: List[DTOModel] = dto_repository.find(
                dto_model_cls,
                conditions,
                offset,
                limit,
                **extra,
            )
            
            return [result_item.to_data_model() for result_item in result]
        except Error as err:
            return err
    
    @classmethod
    def delete(cls, model: Type[DataModel], conditions: dict, limit: int = 1, **extra) -> dict | Error:
        try:
            dto_model_cls: Type[DTOModel] = model._opts.DTO.model
            dto_repository: Type[DTORepository] = model._opts.DTO.model.opts.repository

            result_ids = {
                'count': 0,
                'ids': [],
            }

            result: List[DTOModel] = dto_repository.find(
                dto_model_cls,
                conditions,
                0,
                limit,
                **extra,
            )

            for result_item in result:
                ok = dto_repository.delete(
                    dto_model_cls,
                    result_item.object_id,
                    **extra,
                )

                if ok:
                    result_ids['count'] += 1
                    result_ids['ids'].append(result_item.object_id)

            return result_ids
        except Error as err:
            return err
