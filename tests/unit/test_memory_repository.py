import pytest
from music.domainmodel import user
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User
from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.track import Track

@pytest.fixture
def repo():
    return MemoryRepository()

def test_tracks_are_loaded(repo):
    assert len(repo._MemoryRepository__tracks) > 10

def test_add_get_track(repo):
    track = Track(99999, "834.194")
    repo.add_track(track)
    assert track in repo._MemoryRepository__tracks
    track = repo.get_track(5)
    assert track.track_id == 5
    track = repo.get_track(999999)
    assert track is None

def test_add_get_user(repo):
    user1 = User(1, "ash", "asdaaddf")
    user2 = User(2, "casssi", "asdasdda")
    repo.add_user(user1)
    repo.add_user(user2)
    assert repo._MemoryRepository__users == [user1, user2]
    user3 = repo.get_user("ash")
    assert user3.user_id == 1
    user4 = repo.get_user("ashas")
    assert user4 is None
