from typing import Any, Type, List

from .dto_model import DTOModel


class DTORepository:
    @classmethod
    def save(cls, model: DTOModel, **extra) -> DTOModel:
        raise NotImplementedError()

    @classmethod
    def find(cls, model_cls: Type[DTOModel], conditions: dict, offset: int, limit: int, **extra) -> List[DTOModel]:
        raise NotImplementedError()

    @classmethod
    def delete(cls, model_cls: Type[DTOModel], object_id: str, **extra) -> bool:
        raise NotImplementedError()
