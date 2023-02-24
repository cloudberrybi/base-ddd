from typing import Type

from pydantic import BaseModel

from .data_model import DataModel


class DataFilter(BaseModel):
    from_model: Type[DataModel]
    conditions: dict = {}
    offset: int = 0
    limit: int = 20
