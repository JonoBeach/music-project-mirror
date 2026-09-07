import pytest

from music.authentication.services import AuthenticationException
from music.authentication import services as authentication_services
from music.adapters.memory_repository import MemoryRepository
from music.tracks.services import get_tracks_for_search, get_tracks, get_all_tracks

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

def test_get_tracks(in_memory_repository):
    track1 = Track("Track 1", "Artist 1", "Album 1", 2020)
    track2 = Track("Track 2", "Artist 2", "Album 2", 2021)

    add_track(track1, in_memory_repository)
    add_track(track2, in_memory_repository)

    tracks = get_tracks(in_memory_repository)

    assert len(tracks) == 2
    assert track1 in tracks
    assert track2 in tracks

def test_get_all_tracks(in_memory_repository):
    track1 = Track("Track 1", "Artist 1", "Album 1", 2020)
    track2 = Track("Track 2", "Artist 2", "Album 2", 2021)

    add_track(track1, in_memory_repository)
    add_track(track2, in_memory_repository)

    tracks = get_all_tracks(in_memory_repository)

    assert len(tracks) == 2
    assert track1 in tracks
    assert track2 in tracks

