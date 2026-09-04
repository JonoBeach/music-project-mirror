import pytest
from music.templates.memory_repository import MemoryRepository
from music.domainmodel.track import Track

@pytest.fixture
def repo():
    return MemoryRepository()

def test_tracks_are_loaded(repo):
    assert len(repo._MemoryRepository__tracks) > 10

def test_get_track(repo):
    track = repo.get_track(5)
    assert track.track_id == 5
