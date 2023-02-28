import pytest

from ..interfaces.data_models import User


@pytest.fixture
def simple_data_user():
    return User(
        email='test_1@test1.com'
    )
