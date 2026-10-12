from sqlalchemy import select, inspect
# from sqlalchemy.orm import registry
from music.adapters.orm import mapper_registry, track_genre_table


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    tables = inspector.get_table_names()

    assert 'track' in tables
    assert 'album' in tables
    assert 'artist' in tables

    assert inspector.get_table_names() == ['album', 'artist', 'favourite', 'genre', 'review', 'track', 'track_genre', 'user']


def test_database_populate_all_tracks(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    # tracks table is at index 5 alphabetically
    tracks_table_name = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table tracks
        select_statement = select(mapper_registry.metadata.tables[tracks_table_name])
        result = connection.execute(select_statement)

        tracks = []
        for row in result:
            tracks.append((row[0], row[1]))

        assert len(tracks) == 2000
        # check the first track in the list which is track_id 2 and title 'Food'
        assert tracks[0] == (2, 'Food')


def test_database_populate_all_albums(database_engine):
    inspector = inspect(database_engine)
    albums_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[albums_table_name])
        result = connection.execute(select_statement)

        albums = []
        for row in result:
            albums.append((row[0], row[1]))

        assert len(albums) == 427
        assert albums[0] == (1, 'AWOL - A Way Of Life')


def test_database_populate_all_artists(database_engine):
    inspector = inspect(database_engine)
    artists_table_name = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[artists_table_name])
        result = connection.execute(select_statement)

        artists = []
        for row in result:
            artists.append((row[0], row[1]))

        assert len(artists) == 263
        assert artists[0] == (1, 'AWOL')


def test_database_populate_all_genres(database_engine):
    inspector = inspect(database_engine)
    genres_table_name = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[genres_table_name])
        result = connection.execute(select_statement)

        genres = []
        for row in result:
            genres.append((row[0], row[1]))

        assert len(genres) == 60
        assert genres[0] == (1, 'Avant-Garde')

def test_database_populate_all_track_genres(database_engine):
    inspector = inspect(database_engine)
    track_genres_table_name = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[track_genres_table_name])
        result = connection.execute(select_statement)

        track_genres = []
        for row in result:
            track_genres.append((row[0], row[1]))

        assert len(track_genres) == 2268
        assert (1898, 12) in track_genres
