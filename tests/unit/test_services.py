import pytest

from music.authentication.services import AuthenticationException
from music.authentication import services as authentication_services
from music.domainmodel import track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.tracks import services as tracks_services
from music.adapters.memory_repository import MemoryRepository
from music.favourites import services as favourites_services

@pytest.fixture
def in_memory_repository():
    repository = MemoryRepository()
    return repository

class TestAuthenticationServices:
    def test_add_user(self, in_memory_repository):
        new_username = "test"
        new_password = "Test1234"

        authentication_services.add_user(new_username, new_password, in_memory_repository)
        user_as_dictionary = authentication_services.get_user(new_username, in_memory_repository)

        assert user_as_dictionary['username'] == new_username

        # test that the password has been encrypted
        assert user_as_dictionary['password'].startswith('scrypt:32768')


    def test_cannot_add_user_with_existing_name(self, in_memory_repository):
        username = 'test'
        password = 'Test1234'

        # add once before so it raises error
        authentication_services.add_user(username, password, in_memory_repository)

        with pytest.raises(authentication_services.UsernameAlreadyTakenException):
            authentication_services.add_user(username, password, in_memory_repository)


    def test_authentication_with_valid_credentials(self, in_memory_repository):
        new_username = 'test'
        new_password = 'Test1234'

        authentication_services.add_user(new_username, new_password, in_memory_repository)

        try:
            authentication_services.authenticate_user(new_username, new_password, in_memory_repository)
        except AuthenticationException:
            assert False


    def test_authentication_with_invalid_credentials(self, in_memory_repository):
        new_username = 'test'
        new_password = 'Test1234'

        authentication_services.add_user(new_username, new_password, in_memory_repository)

        with pytest.raises(authentication_services.AuthenticationException):
            authentication_services.authenticate_user(new_username, '00000000', in_memory_repository)


    def test_authentication_is_case_insensitive(self, in_memory_repository):
        new_username = 'test'
        new_password = 'Test1234'
        diff_case_username = 'TeSt'

        authentication_services.add_user(new_username, new_password, in_memory_repository)

        try:
            authentication_services.authenticate_user(diff_case_username, new_password, in_memory_repository)
        except AuthenticationException:
            assert False


class TestTrackServices:
    def test_get_tracks_return_data(self, in_memory_repository):
        tracks, page, total_pages = tracks_services.get_tracks(in_memory_repository, page=1)

        #check if page, len(tracks), total_pages correct
        assert page == 1
        assert len(tracks) <= tracks_services.TRACKS_PER_PAGE
        assert total_pages >= 1

        #track title should already be sorted
        titles = [track.title for track in tracks]
        assert titles == sorted(titles)


    def test_page_out_of_range(self, in_memory_repository):
        tracks, page, total_pages = tracks_services.get_tracks(in_memory_repository, page=500)
        #page number too high, page should be total page
        assert page == total_pages

        tracks, page, total_pages = tracks_services.get_tracks(in_memory_repository, page=-1)
        #page number too low,, page should be 1
        assert page == 1


    def test_get_all_tracks(self, in_memory_repository):
        all_tracks = tracks_services.get_all_tracks(in_memory_repository)
        #test if get_all_tracks gets tracks data in csv
        assert len(all_tracks) > 100

        titles = [t.title for t in all_tracks]
        #test if the track list is sorted alphabetically
        assert titles == sorted(titles)


    def test_search_by_title(self, in_memory_repository):
        track1 = Track(1, "Aoi")
        track2 = Track(4, "Aoi")

        all_tracks = tracks_services.get_all_tracks(in_memory_repository)
        all_tracks.append(track1)
        all_tracks.append(track2)

        tracks, page, total_pages = tracks_services.get_tracks_for_search(
            all_tracks, page=1, search_term="Aoi", search_type="title"
        )
        #should return track1 and track2
        assert len(tracks) == 2
        assert tracks[0].title == "Aoi"


    def test_search_by_artist(self, in_memory_repository):
        track1 = Track(1, "Aoi")
        track2 = Track(4, "M")
        artist1 = Artist(999, "sakanaction")
        track1.artist, track2.artist = artist1, artist1

        all_tracks = tracks_services.get_all_tracks(in_memory_repository)
        all_tracks.append(track1)
        all_tracks.append(track2)

        tracks, page, total_pages = tracks_services.get_tracks_for_search(
            all_tracks, page=1, search_term="sakanaction", search_type="artist"
        )
        #should return track1 and track2
        assert len(tracks) == 2
        assert tracks[1].artist == artist1


    def test_search_by_album(self, in_memory_repository):
        track1 = Track(1, "Aoi")
        track2 = Track(4, "M")
        album1 = Album(999, "sakanaction")
        track1.album, track2.album = album1, album1

        all_tracks = tracks_services.get_all_tracks(in_memory_repository)
        all_tracks.append(track1)
        all_tracks.append(track2)

        tracks, page, total_pages = tracks_services.get_tracks_for_search(
            all_tracks, page=1, search_term="sakanaction", search_type="album"
        )
        #should return track1 and track2
        assert len(tracks) == 2
        assert tracks[0].title == "Aoi"


    def test_search_no_result(self, in_memory_repository):
        all_tracks = tracks_services.get_all_tracks(in_memory_repository)
        tracks, page, total_pages = tracks_services.get_tracks_for_search(
            all_tracks, page=1, search_term="dasdasdada", search_type="title"
        )
        #should be empty list
        assert tracks == []
        assert total_pages == 0


    def test_search_empty_term_returns_all(self, in_memory_repository):
        all_tracks = tracks_services.get_all_tracks(in_memory_repository)
        tracks, page, total_pages = tracks_services.get_tracks_for_search(
            all_tracks, page=1, search_term="", search_type="title"
        )
        #should return all tracks
        assert len(tracks) <= tracks_services.TRACKS_PER_PAGE
        assert total_pages == 134


    def test_get_track_by_id(self, in_memory_repository):
        track1 = tracks_services.get_track_by_id(5, in_memory_repository)
        assert track1 is not None
        assert track1.track_id == 5

    def test_get_track_by_id_not_found(self, in_memory_repository):
        track1 = tracks_services.get_track_by_id(1, in_memory_repository)
        assert track1 is None


    def test_get_review_by_rating(self, in_memory_repository):
        track1 = Track(1, "mellow")
        user = User(1, "sakana", "asdfghjk")
        r1 = Review(1, 1, track1, 2, "not bad", 10)
        r2 = Review(2, 1, track1, 5, "great", 11)
        r3 = Review(3, 1, track1, 3, "good", 1)

        repo = in_memory_repository
        repo.add_user(user)
        repo.add_track(track1)
        repo.add_review(user, r1, track1)
        repo.add_review(user, r2, track1)
        repo.add_review(user, r3, track1)

        reviews = tracks_services.get_review_by_rating(track1, in_memory_repository)
        #test if review order is sorted by rating(high to low)
        assert [r.rating for r in reviews] == [5, 3, 2]


    def test_get_review_by_rating_empty(self, in_memory_repository):
        track1 = Track(1, "Ame")
        in_memory_repository.add_track(track1)

        #should return empty list
        assert tracks_services.get_review_by_rating(
            track1, in_memory_repository) == []


    def test_add_review(self, in_memory_repository):
        user1 = User(1, "username", "password")
        track1 = Track(1, "track")

        in_memory_repository.add_user(user1)
        in_memory_repository.add_track(track1)

        rating = 5
        review_text = "review text"
        date_submitted = 151392262026

        tracks_services.add_review(user1, track1, rating, review_text, date_submitted, in_memory_repository)
        assert len(user1.reviews) == 1


    def test_remove_review(self, in_memory_repository):
        user1 = User(1, "username", "password")
        track1 = Track(1, "track")

        in_memory_repository.add_user(user1)
        in_memory_repository.add_track(track1)

        rating = 5
        review_text = "review text"
        date_submitted = 151392262026

        tracks_services.add_review(user1, track1, rating, review_text, date_submitted, in_memory_repository)
        assert len(user1.reviews) == 1

        review = user1.reviews[0]
        tracks_services.remove_review(user1, review, in_memory_repository)
        assert len(user1.reviews) == 0


class TestFavouritesServices:
    def test_add_favourite(self, in_memory_repository):
        track1 = Track(1, "Ame")
        user1 = User(1, "asd", "asdfafga")

        in_memory_repository.add_user(user1)
        in_memory_repository.add_track(track1)

        favourites_services.add_favourite(user1, track1)
        assert len(user1.favourites) == 1
        assert user1.favourites[0].track == track1


    def test_add_duplicate_favourite(self, in_memory_repository):
        track1 = Track(1, "Ame")
        user1 = User(1, "asd", "asdfafga")

        in_memory_repository.add_user(user1)
        in_memory_repository.add_track(track1)

        favourites_services.add_favourite(user1, track1)
        #should do nothing
        favourites_services.add_favourite(user1, track1)

        assert len(user1.favourites) == 1


    def test_remove_favourite(self, in_memory_repository):
        track1 = Track(1, "Ame")
        user1 = User(1, "asd", "asdfafga")

        in_memory_repository.add_user(user1)
        in_memory_repository.add_track(track1)

        favourites_services.add_favourite(user1, track1)
        assert len(user1.favourites) == 1

        favou = user1.favourites[0]
        favourites_services.remove_favourite(user1, favou)
        assert len(user1.favourites) == 0
