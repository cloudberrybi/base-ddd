import pytest

from ..interfaces.dto_models import EmptyDTO


def test_dto_empty_from_data_model():
    with pytest.raises(NotImplementedError):
        EmptyDTO.from_data_model(None)

def test_dto_empty_to_data_model():
    dto_object = EmptyDTO()

    with pytest.raises(NotImplementedError):
        dto_object.to_data_model()
