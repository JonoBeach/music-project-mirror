import pytest

from music.authentication.services import AuthenticationException
from music.authentication import services as authentication_services
from music.adapters.memory_repository import MemoryRepository


@pytest.fixture
def in_memory_repository():
    repository = MemoryRepository()
    return repository


def test_add_user(in_memory_repository):
    new_username = "test"
    new_password = "Test1234"

    authentication_services.add_user(new_username, new_password, in_memory_repository)
    user_as_dictionary = authentication_services.get_user(new_username, in_memory_repository)
    
    assert user_as_dictionary['username'] == new_username

    # test that the password has been encrypted
    assert user_as_dictionary['password'].startswith('scrypt:32768')


def test_cannot_add_user_with_existing_name(in_memory_repository):
    username = 'test'
    password = 'Test1234'

    # add once before so it raises error
    authentication_services.add_user(username, password, in_memory_repository)

    with pytest.raises(authentication_services.UsernameAlreadyTakenException):
        authentication_services.add_user(username, password, in_memory_repository)
