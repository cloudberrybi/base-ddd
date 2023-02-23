from typing import Type

from pydantic import BaseModel

from .dto_model import DTOModel


class DataModelDTOOpts(BaseModel):
    model: Type[DTOModel]
