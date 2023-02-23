from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .data_model_opts import DataModelOpts


class DataModel(BaseModel):
    _opts: DataModelOpts

    object_id: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
