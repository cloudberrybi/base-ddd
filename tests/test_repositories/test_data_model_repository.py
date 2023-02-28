import time

from cbi_ddd.repositories import (
    StubDTORepository,
    StorageRepository,
)
from cbi_ddd.interfaces import (
    errors,
)

from ..fixtures.dramatiq import (
    stub_broker,
    stub_worker,
)
from ..fixtures.settings import (
    settings_with_rmq_full_config
)
from ..interfaces.data_models import (
    User,
)
from ..interfaces.dto_models import (
    UserDTO
)
from ..interfaces.data_model_repositories import UserRepository


def test_save_user_repository(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    user = UserRepository.save(
        email='test123@test123.com',
    )

    finded_users = StubDTORepository.find(UserDTO, {'email': 'test123@test123.com'}, 0, 1)

    assert user.object_id == finded_users[0].object_id

def test_usave_user_repository(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    UserRepository.usave(
        email='test123.1@test123.com',
    )

    time.sleep(3)

    finded_users = StubDTORepository.find(UserDTO, {'email': 'test123.1@test123.com'}, 0, 10)

    assert len(finded_users) == 1

def test_save_user_repository_error(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    user = UserRepository.save(
        extra={
            'save_error': True,
        },
        email='test123@test1230.com',
    )

    assert isinstance(user, errors.SaveError)

def test_get_user_repository(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    user = StorageRepository.save(User(
        email='test124@test123.com',
    ))

    getted_user = UserRepository.get({'email': 'test124@test123.com'})

    assert user.object_id == getted_user.object_id

def test_get_user_repository_error(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    user = StorageRepository.save(User(
        email='test124@test1231.com',
    ))

    getted_user = UserRepository.get({'email': 'test124@test123.com'}, find_error=True)

    assert isinstance(getted_user, errors.FindError)

def test_find_users_repository(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    for i in range(157):
        StorageRepository.save(User(
            email=f'test{i}@test124.com',
            first_name='Alex-Alex',
        ))

    finded_users_0 = UserRepository.find({'first_name': 'Alex-Alex'}, 0, 67)
    finded_users_1 = UserRepository.find({'first_name': 'Alex-Alex'}, 67, 113)

    assert len(finded_users_0) == 67
    assert len(finded_users_1) == 90

def test_find_users_repository_error(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    for i in range(157):
        StorageRepository.save(User(
            email=f'test{i}@test1241.com',
            first_name='Alex-Alex-Alex',
        ))

    finded_users_0 = UserRepository.find({'first_name': 'Alex-Alex-Alex'}, 0, 67, find_error=True)
    finded_users_1 = UserRepository.find({'first_name': 'Alex-Alex-Alex'}, 67, 113)

    assert isinstance(finded_users_0, errors.FindError)
    assert len(finded_users_1) == 90

def test_delete_users_repository(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    user = StorageRepository.save(User(
        email=f'test123@test125.com',
        first_name='Berth',
    ))

    assert UserRepository.get({'object_id': user.object_id}) is not None

    UserRepository.delete({'object_id': user.object_id})

    assert UserRepository.get({'object_id': user.object_id}) is None

def test_udelete_users_repository(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    user = StorageRepository.save(User(
        email=f'test123@test125.com',
        first_name='Berth',
    ))

    assert UserRepository.get({'object_id': user.object_id}) is not None

    UserRepository.udelete({'object_id': user.object_id})
    time.sleep(3)

    assert UserRepository.get({'object_id': user.object_id}) is None

def test_delete_users_repository_error(mocker, settings_with_rmq_full_config, stub_broker, stub_worker):
    mocker.patch('cbi_ddd.repositories.SettingsRepository.get_config', return_value=settings_with_rmq_full_config)

    UserRepository.init_actors()

    user = StorageRepository.save(User(
        email=f'test123@test1251.com',
        first_name='Berth-Berth',
    ))

    assert UserRepository.get({'object_id': user.object_id}) is not None

    result = UserRepository.delete({'object_id': user.object_id}, delete_error=True)

    assert UserRepository.get({'object_id': user.object_id}) is not None
    assert isinstance(result, errors.DeleteError)
