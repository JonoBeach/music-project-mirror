import pytest
from music.domainmodel import user
from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.adapters.memory_repository import MemoryRepository

@pytest.fixture
def repo():
    return MemoryRepository()

def test_tracks_are_loaded(repo):
    assert len(repo._MemoryRepository__tracks) > 10

def test_add_get_track(repo: MemoryRepository):
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

def test_add_remove_favourite(repo:MemoryRepository):
    user1 = User(1, "ash", "asdaaddf")
    track1 = Track(1, "track")
    favo1 = Favourite(1, 1, track1)
    favo2 = Favourite(2, 1, track1)
    repo.add_user(user1)
    repo.add_favourite(user1, favo1)
    repo.add_favourite(user1, favo2)
    assert repo.get_user_favourite(user1) == [favo1]

def test_review_function(repo:MemoryRepository):
    user1 = User(1, "ash", "asdadadad")
    user2 = User(2, "asda", "dadsdadad")
    user3 = User(3, "asaad", "adasdafafa")
    track = repo.get_track(5)
    review1 = Review(1, 1, track, 1, "first review", 1)
    review2 = Review(2, 2, track, 2, "second review", 2)
    review3 = Review(3, 3, track, 3, "third review", 3)
    repo.add_review(user1, review1, track)
    repo.add_review(user2, review2, track)
    repo.add_review(user3, review3, track)
    assert repo.get_review_by_date(track) == [review1, review2, review3]
    assert repo.get_review_by_rating(track) == [review3, review2, review1]
    assert len(user1.reviews) == len(user2.reviews) == len(user3.reviews) == 1
    repo.remove_review(user2, review2, track)
    assert repo.get_review_by_date(track) == [review1, review3]
    assert repo.get_review_by_rating(track) == [review3, review1]
    assert len(user2.reviews) == 0
