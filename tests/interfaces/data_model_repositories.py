from cbi_ddd.interfaces import DataModelRepository

from .data_models import User


class UserRepository(DataModelRepository):
    repository_id = 'user'
    model = User
