from typing import List, Any, Optional

from cbi_ddd.interfaces import DTOModel
from cbi_ddd.repositories import StubDTORepository


class EmptyDTO(DTOModel):
    pass


class UserRoleDTO(DTOModel):
    class opts:
        tablename = 'user_roles'
        repository = StubDTORepository

    name: str

    @classmethod
    def from_data_model(cls, model) -> 'UserRoleDTO':
        return cls(
            object_id=model.object_id,
            created=model.created,
            updated=model.updated,
            name=model.name,
        )
    
    def to_data_model(self) -> Any:
        from .data_models import UserRole

        return UserRole(
            object_id=self.object_id,
            created=self.created,
            updated=self.updated,
            name=self.name,
        )


class UserTagDTO(DTOModel):
    class opts:
        tablename = 'user_tags'
        repository = StubDTORepository

    name: str

    @classmethod
    def from_data_model(cls, model) -> 'UserRoleDTO':
        return cls(
            object_id=model.object_id,
            created=model.created,
            updated=model.updated,
            name=model.name,
        )
    
    def to_data_model(self) -> Any:
        from .data_models import UserTag

        return UserTag(
            object_id=self.object_id,
            created=self.created,
            updated=self.updated,
            name=self.name,
        )



class UserDTO(DTOModel):
    class opts:
        tablename = 'users'
        repository = StubDTORepository
        foreign_fields = {
            'roles': UserRoleDTO,
            'tag': UserTagDTO,
        }

    email: str
    first_name: str
    last_name: str
    tag: Optional[str]
    roles: List[str] = []

    @classmethod
    def from_data_model(cls, model) -> 'UserDTO':
        return cls(
            object_id=model.object_id,
            created=model.created,
            updated=model.updated,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            tag=model.tag.object_id if model.tag else None,
            roles=[ role.object_id for role in model.roles ],
        )

    def to_data_model(self) -> Any:
        from .data_models import User

        return User(
            object_id=self.object_id if self.object_id else '',
            created=self.created,
            updated=self.updated,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            tag=self.fill_foreign_field('tag'),
            roles=self.fill_foreign_list_field('roles'),
        )
