from sqlalchemy import text

from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre


def make_track() -> Track:
    track = Track(2, "Shivers")
    track.track_url = 'http://freemusicarchive.org/music/shivers'
    track.track_duration = 200
    track.album = make_album()
    track.artist = make_artist()
    return track


def make_genre() -> Genre:
    genre = Genre(1, 'Pop')
    return genre


def make_album() -> Album:
    album = Album(1, '=')
    album.album_url = 'http://freemusicarchive.org/music/albums/='
    album.album_type = 'Album'
    album.release_year = 2022
    return album


def make_artist():
    artist = Artist(1, 'Ed Sheeran')
    return artist


def insert_track(empty_session, track: Track):
    empty_session.execute(
        text(
            'INSERT INTO tracks (track_id, title, track_url, track_duration) VALUES '
            f'({track.track_id}, "{track.title}", '
            f'"{track.track_url}", {track.track_duration})'
        )
    )
    row = empty_session.execute(text('SELECT track_id from tracks')).fetchone()
    return row[0]


def insert_artist(empty_session, artist: Artist):
    empty_session.execute(
        text(
            'INSERT INTO artists (artist_id, full_name) VALUES '
            f'({artist.artist_id}, "{artist.full_name}")'
        )
    )
    row = empty_session.execute(text('SELECT artist_id from artists')).fetchone()
    return row[0]

def insert_album(empty_session, album: Album):
    empty_session.execute(
        text(
            'INSERT INTO albums (album_id, title) VALUES '
            f'({album.album_id}, "{album.title}")'
        )
    )
    row = empty_session.execute(text('SELECT album_id from albums')).fetchone()
    return row[0]

def test_loading_of_track(empty_session):
    track = make_track()
    track_key = insert_track(empty_session, track)
    fetched_track = empty_session.query(Track).one()

    assert track_key == fetched_track.track_id
    assert track == fetched_track


def test_saving_of_track(empty_session):
    track = make_track()
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT title, track_url, track_duration, artist_id, album_id FROM tracks')))

    assert rows == [(track.title, track.track_url, track.track_duration,
                     track.artist.artist_id, track.album.album_id)]

def test_loading_of_artists(empty_session):
    artist = make_artist()
    artist_key = insert_artist(empty_session, artist)
    fetched_artist = empty_session.query(Artist).one()

    # Confirm the fetched artist has the same id as expected
    assert artist_key == fetched_artist.artist_id
    # Test the fetched artist is identical to the artist we created in advance
    assert artist == fetched_artist


def test_saving_of_artist(empty_session):
    artist = make_artist()
    empty_session.add(artist)
    empty_session.commit()

    # Fetch the artist we just added
    rows = list(empty_session.execute(
        text('SELECT artist_id, full_name FROM artists')))

    # Confirm all the artist attributes were saved successfully
    assert rows == [(artist.artist_id, artist.full_name)]


def test_artist_track_relationship(empty_session):
    artist = make_artist()
    track = make_track()
    track.artist = artist

    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT track_id, artist_id FROM tracks')))
    assert rows == [(track.track_id, artist.artist_id)]


def test_loading_of_albums(empty_session):
    album = make_album()
    album_key = insert_album(empty_session, album)
    fetched_album = empty_session.query(Album).one()

    # Confirm the fetched artist has the same id as expected
    assert album_key == fetched_album.album_id
    # Test the fetched artist is identical to the artist we created in advance
    assert album == fetched_album



def test_saving_of_albums(empty_session):
    album = make_album()
    empty_session.add(album)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT album_id, title FROM albums')))

    assert rows == [(album.album_id, album.title)]


def test_album_track_relationship(empty_session):
    album = make_album()
    track = make_track()
    track.album = album

    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT track_id, album_id FROM tracks')))
    assert rows == [(track.track_id, album.album_id)]


def test_loading_of_tracks_with_genres(empty_session):
    track = make_track()
    genre = make_genre()
    track.add_genre(genre)

    track_key = insert_track(empty_session, track)
    fetched_track = empty_session.query(Track).one()

    assert track_key == fetched_track.track_id
    assert track == fetched_track
    assert genre in track.genres


def test_saving_of_tracks_with_genres(empty_session):
    track = make_track()
    genre = make_genre()
    track.add_genre(genre)

    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute(
        text('SELECT track_id, genre_id FROM track_genres')))
    assert rows == [(track.track_id, genre.genre_id)]
