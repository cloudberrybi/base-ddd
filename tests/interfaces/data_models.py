from typing import List, Optional

from cbi_ddd.interfaces import (
    DataModel,
    DataModelOpts,
    DataModelDTOOpts,
)

from .dto_models import (
    UserDTO,
    UserRoleDTO,
    UserTagDTO,
)


class UserRole(DataModel):
    _opts = DataModelOpts(
        DTO=DataModelDTOOpts(
            model=UserRoleDTO,
        )
    )

    name: str

class UserTag(DataModel):
    _opts = DataModelOpts(
        DTO=DataModelDTOOpts(
            model=UserTagDTO,
        )
    )

    name: str


class User(DataModel):
    _opts = DataModelOpts(
        DTO=DataModelDTOOpts(
            model=UserDTO,
        )
    )

    email: str
    first_name: str = ''
    last_name: str = ''
    tag: Optional[UserTag]
    roles: List[UserRole] = []
