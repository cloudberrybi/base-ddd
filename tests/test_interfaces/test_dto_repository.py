import pytest

from ..interfaces import (
    EmptyDTO,
    EmptyDTORepository,
)


def test_dto_repository_empty_save():
    dto_object = EmptyDTO()

    with pytest.raises(NotImplementedError):
        EmptyDTORepository.save(dto_object)

def test_dto_repository_empty_find():
    with pytest.raises(NotImplementedError):
        EmptyDTORepository.find(EmptyDTO, {}, 0, 100)

def test_dto_repository_empty_delete():
    with pytest.raises(NotImplementedError):
        EmptyDTORepository.delete(EmptyDTO, '')
