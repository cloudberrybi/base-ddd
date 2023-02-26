from cbi_ddd.repositories import StorageRepository, StubDTORepository
from cbi_ddd.interfaces.errors import StubError, InitStorageError

from ..fixtures.data_models import simple_data_user
from ..interfaces.data_models import User, UserRole, UserTag


def test_save(simple_data_user):
    user = StorageRepository.save(simple_data_user)

    assert StubDTORepository.is_exists(user._opts.DTO.model.opts.tablename, user.object_id)

def test_save_return_error(simple_data_user):
    result = StorageRepository.save(simple_data_user, save_error = True)
    assert isinstance(result, StubError)

def test_save_return_init_error(simple_data_user):
    result = StorageRepository.save(simple_data_user, init_error = True)
    assert isinstance(result, InitStorageError)

def test_save_object_with_foreign_list_fields():
    roles_str = [
        'test_role_1',
        'test_role_2',
    ]
    roles_arr = []

    for role_str_item in roles_str:
        roles_arr.append(StorageRepository.save(UserRole(
            name=role_str_item,
        )))

    user = StorageRepository.save(User(
        email='test5@test4.com',
        roles=roles_arr,
    ))

    finded_user = StorageRepository.get(User, {
        'object_id': user.object_id,
    })

    assert finded_user.roles == roles_arr

def test_save_object_with_foreign_field(simple_data_user):
    user_tag = StorageRepository.save(
        UserTag(
            name='test_tag',
        )
    )

    simple_data_user.tag = user_tag
    simple_data_user = StorageRepository.save(simple_data_user)
    finded_user = StorageRepository.get(User, {
        'object_id': simple_data_user.object_id,
    })

    assert finded_user.tag.name == user_tag.name


def test_get(simple_data_user):
    user = StorageRepository.save(simple_data_user)

    getted_user = StorageRepository.get(User, {'object_id': user.object_id})
    assert getted_user.email == user.email

def test_get_return_error(simple_data_user):
    user = StorageRepository.save(simple_data_user)

    result = StorageRepository.get(User, {'object_id': user.object_id}, find_error=True)
    assert isinstance(result, StubError)

def test_delete(simple_data_user):
    user = StorageRepository.save(simple_data_user)

    assert StubDTORepository.is_exists(user._opts.DTO.model.opts.tablename, user.object_id)

    StorageRepository.delete(User, {'object_id': user.object_id})

    assert not StubDTORepository.is_exists(user._opts.DTO.model.opts.tablename, user.object_id)

def test_delete_with_conditions():
    StorageRepository.save(User(
        email='test1@test.com',
        first_name='Test1',
    ))
    StorageRepository.save(User(
        email='test2@test.com',
        first_name='Test1',
    ))

    assert len(StorageRepository.find(User, {
        'first_name': 'Test1'
    }, 0, 100)) == 2

    StorageRepository.delete(User, {
        'first_name': 'Test1'
    }, limit=2)

    assert len(StorageRepository.find(User, {
        'first_name': 'Test1'
    }, 0, 100)) == 0

def test_delete_with_conditions_and_limit():
    for i in range(10):
        StorageRepository.save(User(
            email=f'test{i}@test.com',
            first_name='Test2',
        ))

    assert len(StorageRepository.find(User, {
        'first_name': 'Test2'
    }, 0, 100)) == 10

    StorageRepository.delete(User, {
        'first_name': 'Test2'
    }, limit=7)

    assert len(StorageRepository.find(User, {
        'first_name': 'Test2'
    }, 0, 100)) == 3

def test_delete_return_error(simple_data_user):
    user = StorageRepository.save(simple_data_user)

    result = StorageRepository.delete(User, {'object_id': user.object_id}, delete_error = True)
    print(result)
    assert isinstance(result, StubError)

def test_find():
    for i in range(100):
        StorageRepository.save(User(
            email=f'test{i}@test3.com',
            first_name='Test4',
        ))

    finded_users_p0 = StorageRepository.find(User, {'first_name': 'Test4'}, 0, 67)
    finded_users_p1 = StorageRepository.find(User, {'first_name': 'Test4'}, 67, 67)

    assert len(finded_users_p0) == 67
    assert len(finded_users_p1) == 33
