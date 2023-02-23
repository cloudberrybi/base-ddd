from typing import List, Optional

from pydantic import BaseModel

from .data_model_dto_opts import DataModelDTOOpts


class DataModelOpts(BaseModel):
    DTO: DataModelDTOOpts
    unique_fields: Optional[List[str]] = []
