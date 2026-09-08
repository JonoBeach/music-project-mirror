import pytest
from music.adapters.memory_repository import MemoryRepository
from music.adapters import repository
from music.domainmodel.track import Track
from music.tracks import services

@pytest.fixture
def repo():
    repo = MemoryRepository()
    repository.repo_instance = repo
    return repo

def test_get_tracks_return_data(repo:MemoryRepository):
    tracks, page, total_pages = services.get_tracks(page=1)

    #check if page, len(tracks), total_pages correct
    assert page == 1
    assert len(tracks) <= services.TRACKS_PER_PAGE
    assert total_pages >= 1
    #track title should already be sorted
    titles = [track.title for track in tracks]
    assert titles == sorted(titles)

def test_page_out_of_range(repo:MemoryRepository):
    tracks, page, total_pages = services.get_tracks(page=500)
    #page should be total page
    assert page == total_pages
