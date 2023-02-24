from typing import Any, Type, List

from .dto_model import DTOModel


class DTORepository:
    @classmethod
    def save(cls, model: DTOModel) -> DTOModel:
        pass

    @classmethod
    def find(cls, model_cls: Type[DTOModel], conditions: dict, offset: int, limit: int) -> List[DTOModel]:
        pass

    @classmethod
    def delete(cls, model_cls: Type[DTOModel], object_id: str) -> bool:
        pass
