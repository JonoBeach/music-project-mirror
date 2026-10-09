import pytest
from music.adapters.repository import repo_instance
from music.domainmodel import user
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.favourite import Favourite
from music.domainmodel.genre import Genre
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
    assert track.id == 5

    #no track found, should return None
    track = repo.get_track(999999)
    assert track is None

def test_add_get_user(repo):
    user1 = User(1, "ash", "asdaaddf")
    user2 = User(2, "casssi", "asdasdda")
    repo.add_user(user1)
    repo.add_user(user2)
    assert repo._MemoryRepository__users == [user1, user2]

    user3 = repo.get_user("ash")
    assert user3.id == 1

    #no user found, should return None
    user4 = repo.get_user("ashas")
    assert user4 is None

def test_add_remove_favourite(repo:MemoryRepository):
    user1 = User(1, "ash", "asdaaddf")
    track1 = Track(1, "track1")
    track2 = Track(2, "track2")
    favo1 = Favourite(1, user1.id, track1)
    favo2 = Favourite(2, user1.id, track1)
    favo3 = Favourite(3, user1.id, track2)
    repo.add_user(user1)

    repo.add_favourite(user1, favo1)
    assert repo.get_user_favourites(user1) == [favo1]

    #favo1 and favou2 have same track, should do nothing
    repo.add_favourite(user1, favo2)
    assert repo.get_user_favourites(user1) == [favo1]

    repo.add_favourite(user1, favo3)
    assert repo.get_user_favourites(user1) == [favo1, favo3]

    repo.remove_favourite(user1, favo3)
    assert repo.get_user_favourites(user1) == [favo1]

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

    #test two sort function and add_review function
    assert repo.get_reviews_by_date(track) == [review1, review2, review3]
    assert repo.get_reviews_by_rating(track) == [review3, review2, review1]
    assert len(user1.reviews) == len(user2.reviews) == len(user3.reviews) == 1

    #test remove function
    repo.remove_review(user2, review2, track)
    assert repo.get_reviews_by_date(track) == [review1, review3]
    assert repo.get_reviews_by_rating(track) == [review3, review1]
    assert len(user2.reviews) == 0

def test_sort_by_title(repo:MemoryRepository):
    list = repo.sort_by_track_title()

    #use a sorted str list to compare with title list
    title_list = [track.title for track in list]
    assert title_list == sorted(title_list)

def test_search_method(repo:MemoryRepository):
    track1 = Track(1, "Song Silly")
    repo.add_track(track1)

    assert [track1] == repo.search_by_title("Song Silly")
    #test case-insisitive, partial match
    assert [track1] == repo.search_by_title("silly")
    #test not found case
    assert repo.search_by_title("dahgdhagd") == []

    genre = Genre(9999, "Wild Genre")
    track1.add_genre(genre)

    assert repo.search_by_genre("Wild Genre") == [track1]
    assert repo.search_by_genre("wild") == [track1]
    assert repo.search_by_genre("asdafa") == []

    artist = Artist(9999, "toe")
    track1.artist = artist

    assert repo.search_by_artist("toe") == [track1]
    assert repo.search_by_artist("TOE") == [track1]
    assert repo.search_by_artist("adsdafaga") == []

    album = Album(9999, "Hear You")
    track1.album = album

    assert repo.search_by_album("Hear You") == [track1]
    assert repo.search_by_album("Hear y") == [track1]
    assert repo.search_by_album("sdadsaf") == []
