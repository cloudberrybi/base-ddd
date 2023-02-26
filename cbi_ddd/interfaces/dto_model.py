from datetime import datetime
from typing import Any, Optional, List

from pydantic import BaseModel

from cbi_ddd.interfaces.errors import Error


class DTOModel(BaseModel):
    class opts:
        tablename = 'dto_model'
        indexes = []
        repository: Any
        foreign_fields = {}

    object_id: Optional[str]
    updated: Optional[datetime]
    created: Optional[datetime]

    @classmethod
    def from_data_model(cls, model) -> Any:
        raise NotImplementedError()

    def to_data_model(self) -> Any:
        raise NotImplementedError()

    def fill_foreign_list_field(self, field: str) -> List[Any]:
        items = []

        foreign_dto_model = self.opts.foreign_fields.get(field, None)
        if foreign_dto_model:
            for item_str in getattr(self, field, []):
                items_dto = self.opts.repository.find(
                    model_cls=foreign_dto_model,
                    conditions={
                        'object_id': item_str
                    },
                    offset=0,
                    limit=1,
                )

                if not isinstance(items_dto, Error) and len(items_dto) > 0:
                    items.append(items_dto[0].to_data_model())

        return items
    
    def fill_foreign_field(self, field: str) -> Any | None:
        foreign_dto_model = self.opts.foreign_fields.get(field, None)
        if foreign_dto_model:
            item_str = getattr(self, field, None)
            items_dto = self.opts.repository.find(
                model_cls=foreign_dto_model,
                conditions={
                    'object_id': item_str
                },
                offset=0,
                limit=1,
            )

            if not isinstance(items_dto, Error) and len(items_dto) > 0:
                return items_dto[0].to_data_model()
        
        return None
