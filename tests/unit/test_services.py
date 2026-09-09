import pytest

from music.authentication.services import AuthenticationException
from music.authentication import services as authentication_services
from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.tracks import services as tracks_services

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


def test_authentication_with_valid_credentials(in_memory_repository):
    new_username = 'test'
    new_password = 'Test1234'

    authentication_services.add_user(new_username, new_password, in_memory_repository)

    try:
        authentication_services.authenticate_user(new_username, new_password, in_memory_repository)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repository):
    new_username = 'test'
    new_password = 'Test1234'

    authentication_services.add_user(new_username, new_password, in_memory_repository)

    with pytest.raises(authentication_services.AuthenticationException):
        authentication_services.authenticate_user(new_username, '00000000', in_memory_repository)

def test_authentication_is_case_insensitive(in_memory_repository):
    new_username = 'test'
    new_password = 'Test1234'
    diff_case_username = 'TeSt'

    authentication_services.add_user(new_username, new_password, in_memory_repository)

    try:
        authentication_services.authenticate_user(diff_case_username, new_password, in_memory_repository)
    except AuthenticationException:
        assert False

def test_add_review():
    user1 = User(1, "username", "password")
    track1 = Track(1, "track")
    rating = 5
    review_text = "review text"
    date_submitted = 151392262026

    tracks_services.add_review(user1, track1, rating, review_text, date_submitted)
    assert len(user1.reviews) == 1

def test_remove_review():
    user1 = User(1, "username", "password")
    track1 = Track(1, "track")
    rating = 5
    review_text = "review text"
    date_submitted = 151392262026

    tracks_services.add_review(user1, track1, rating, review_text, date_submitted)
    assert len(user1.reviews) == 1

    review = user1.reviews[0]
    tracks_services.remove_review(user1, review)
    assert len(user1.reviews) == 0
