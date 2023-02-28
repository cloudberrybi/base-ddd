import pytest

from cbi_ddd.repositories import StubDTORepository
from cbi_ddd.interfaces.errors import InitStorageError, StubError

from ..fixtures.dto_models import (
    simple_user,
    another_simple_user,
)
from ..interfaces.dto_models import UserDTO


def test_raise_init_storage_error(simple_user):
    with pytest.raises(InitStorageError):
        StubDTORepository.save(simple_user, init_error = True)

def test_raise_save_error(simple_user):
    with pytest.raises(StubError):
        StubDTORepository.save(simple_user, save_error = True)

def test_raise_find_error():
    with pytest.raises(StubError):
        StubDTORepository.find(UserDTO, {}, 0, 100, find_error = True)

def test_raise_delere_error():
    with pytest.raises(StubError):
        StubDTORepository.delete(UserDTO, 'test', delete_error = True)

def test_save(simple_user):
    simple_user.object_id = 'test2'
    assert StubDTORepository.is_exists(UserDTO.opts.tablename, 'test2') == False

    StubDTORepository.save(simple_user)

    assert StubDTORepository.is_exists(UserDTO.opts.tablename, 'test2') == True

def test_save_replace(simple_user):
    simple_user.object_id = 'test2.1'
    StubDTORepository.save(simple_user)
    finded_user = StubDTORepository.find(UserDTO, {'object_id': 'test2.1'}, 0, 1)[0]
    assert finded_user.email == 'test@test.com'

    simple_user.email = 'test2@test.com'
    StubDTORepository.save(simple_user)
    finded_user = StubDTORepository.find(UserDTO, {'object_id': 'test2.1'}, 0, 1)[0]
    assert finded_user.email == 'test2@test.com'

def test_delete(simple_user):
    simple_user.object_id = 'test3'

    assert StubDTORepository.is_exists(UserDTO.opts.tablename, 'test3') == False
    StubDTORepository.save(simple_user)
    assert StubDTORepository.is_exists(UserDTO.opts.tablename, 'test3') == True
    assert StubDTORepository.delete(UserDTO, 'test3') == True
    assert StubDTORepository.is_exists(UserDTO.opts.tablename, 'test3') == False

def test_delete_non_existent_id(simple_user):
    simple_user.object_id = 'test3.1'

    StubDTORepository.save(simple_user)
    assert StubDTORepository.delete(UserDTO, 'test_3') == False

def test_find(simple_user):
    simple_user.object_id = 'test4'

    StubDTORepository.save(simple_user)

    finded_user = StubDTORepository.find(UserDTO, {'object_id': 'test4'}, 0, 1)[0]
    assert finded_user.email == simple_user.email

def test_find_many_objects(simple_user, another_simple_user):
    StubDTORepository.save(simple_user)
    StubDTORepository.save(another_simple_user)

    finded_users = StubDTORepository.find(UserDTO, {'email': 'test3@test10.com'}, 0, 10)

    assert len(finded_users) == 1

def test_find_wrong_conditions(simple_user, another_simple_user):
    StubDTORepository.save(simple_user)
    StubDTORepository.save(another_simple_user)

    finded_users = StubDTORepository.find(UserDTO, {'password': '123'}, 0, 10)

    assert len(finded_users) == 0
