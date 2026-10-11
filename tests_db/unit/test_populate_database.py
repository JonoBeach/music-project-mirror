from sqlalchemy import select, inspect
from sqlalchemy.orm import registry


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    tables = inspector.get_table_names()

    assert 'tracks' in tables
    assert 'albums' in tables
    assert 'artists' in tables

    assert inspector.get_table_names() == ['albums', 'artists', 'genres', 'track_genres', 'tracks']


def test_database_populate_all_tracks(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    # tracks table is at index 5 alphabetically
    tracks_table_name = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table tracks
        select_statement = select(registry.metadata.tables[tracks_table_name])
        result = connection.execute(select_statement)

        tracks = []
        for row in result:
            tracks.append((row[0], row[1]))

        assert len(tracks) == 10
        # check the first track in the list which is track_id 2 and title 'Food'
        assert tracks[0] == (2, 'Food')


def test_database_populate_all_albums(database_engine):
    inspector = inspect(database_engine)
    albums_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(registry.metadata.tables[albums_table_name])
        result = connection.execute(select_statement)

        albums = []
        for row in result:
            albums.append((row[0], row[1]))

        assert len(albums) == 5
        assert albums[0] == (1, 'AWOL - A Way Of Life')


def test_database_populate_all_artists(database_engine):
    inspector = inspect(database_engine)
    artists_table_name = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select(registry.metadata.tables[artists_table_name])
        result = connection.execute(select_statement)

        artists = []
        for row in result:
            artists.append((row[0], row[1]))

        assert len(artists) == 5
        assert artists[0] == (1, 'AWOL')


def test_database_populate_all_genres(database_engine):
    inspector = inspect(database_engine)
    genres_table_name = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        select_statement = select(registry.metadata.tables[genres_table_name])
        result = connection.execute(select_statement)

        genres = []
        for row in result:
            genres.append((row[0], row[1]))

        assert len(genres) == 7
        assert genres[0] == (1, 'Avant-Garde')

def test_database_populate_all_track_genres(database_engine):
    inspector = inspect(database_engine)
    track_genres_table_name = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_statement = select(registry.metadata.tables[track_genres_table_name])
        result = connection.execute(select_statement)

        track_genres = []
        for row in result:
            track_genres.append((row[0], row[1]))

        assert len(track_genres) == 14
        assert track_genres[0] == (21, 2)
