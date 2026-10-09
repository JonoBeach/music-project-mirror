from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre

def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = Track(5001, 'New track 1')
    track2 = Track(5002, 'New track 2')
    repo.add_track(track)
    repo.add_track(track2)

    assert repo.get_track(5001) == track
    assert repo.get_track(5002) == track2


def test_repository_can_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track_id = 2
    track = repo.get_track(track_id)

    assert track.title == 'Food'
    assert track.album.title == 'AWOL - A Way Of Life'
    assert track.artist.full_name == 'AWOL'


def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(10201901)
    assert track is None


def test_repository_can_retrieve_track_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_tracks = repo.get_number_of_tracks()

    assert number_of_tracks == 10


def test_repository_can_retrieve_all_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_all_tracks()
    assert len(tracks) == 10

def test_repository_can_get_limited_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks()
    assert len(tracks) == 10

def test_repository_can_add_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album = Album(5001, 'New album 1')
    album2 = Album(5002, 'New album 2')
    repo.add_album(album)
    repo.add_album(album2)

    assert repo.get_album(5001) == album
    assert repo.get_album(5002) == album2


def test_repository_can_retrieve_albums(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album_id = 4
    album = repo.get_album(album_id)

    assert album.title == 'Niris'
    assert album.album_url == 'http://freemusicarchive.org/music/Chris_and_Nicky_Andrews/Niris/'
    assert album.album_type == 'Album'
    assert album.release_year == 2009

def test_repository_can_add_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist = Artist(5001, 'New artist 1')
    artist2 = Artist(5001, 'New artist 2')
    repo.add_artist(artist)
    repo.add_artist(artist2)

    assert artist in repo.get_artists()
    assert artist2 in repo.get_artists()


def test_repository_can_retrieve_artists(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist_id = 1
    artist = repo.get_artist(artist_id)

    assert artist.full_name == 'AWOL'

def test_repository_can_add_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre(5001, 'New genre 1')
    genre2 = Genre(5002, 'New genre 2')
    repo.add_genre(genre)
    repo.add_genre(genre2)

    assert repo.get_genre(5001) == genre
    assert repo.get_genre(5002) == genre2


def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre_id = 1
    genre = repo.get_genre(genre_id)

    assert genre.name == 'Avant-Garde'

# Write a test for checking searching of tracks in the repository by genre name
def test_repository_can_search_tracks_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre_id = '1'
    tracks = repo.get_tracks_by_genre(genre_id)

    assert len(tracks) == 2
    assert tracks[0].title == 'Side A'
    assert tracks[1].title == 'Side B'
