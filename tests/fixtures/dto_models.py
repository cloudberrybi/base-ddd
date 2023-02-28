import pytest

from ..interfaces.dto_models import UserDTO


@pytest.fixture
def simple_user():
    return UserDTO(
        object_id='test1',
        email='test@test.com',
        first_name='John',
        last_name='Doe'
    )

@pytest.fixture
def another_simple_user():
    return UserDTO(
        object_id='test2',
        email='test3@test10.com',
        first_name='Johny',
        last_name='Test'
    )
