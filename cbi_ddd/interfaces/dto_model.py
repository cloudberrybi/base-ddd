from datetime import datetime
from typing import Any, Optional, List

from pydantic import BaseModel


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
        pass

    def to_data_model(self) -> Any:
        pass

    def fill_foreign_list_field(self, field: str) -> List[Any]:
        items = []

        foreign_dto_model = self.opts.foreign_fields.get(field, None)
        if foreign_dto_model:
            for item_str in getattr(self, field, []):
                item_dto = self.opts.repository.get(
                    model_cls=foreign_dto_model,
                    conditions={
                        'object_id': item_str
                    }
                )

                if item_dto:
                    items.append(item_dto.to_data_model())

        return items
    
    def fill_foreign_field(self, field: str) -> Any | None:
        foreign_dto_model = self.opts.foreign_fields.get(field, None)
        if foreign_dto_model:
            item_str = getattr(self, field, None)
            item_dto = self.opts.repository.get(
                model_cls=foreign_dto_model,
                conditions={
                    'object_id': item_str
                }
            )

            if item_dto:
                return item_dto.to_data_model()
        
        return None
