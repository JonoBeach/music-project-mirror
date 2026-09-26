from sqlalchemy import Table, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import registry, relationship
from music.domainmodel import Album, Artist, Favourite, Genre, Review, Track, User

mapper_registry = registry()

album_table = Table(
    "album",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("title", Text),
    Column("release_year", Integer),
    Column("album_url", Text),
    Column("album_info", Text)
)

artist_table = Table(
    "artist",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("full_name", Text)
)

favourite_table = Table(
    "favourite",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable = False, unique = True),
)

genre_table = Table(
    "genre",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable = False)
)

review_table = Table(
    "review",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable = False, unique = True),
    Column("rating", Integer),
    Column("review_text", Text),
    Column("date_submitted", Integer)
)

track_table = Table(
    "track",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("title", Text),
    Column("track_url", Text),
    Column("track_duration", Integer),
)

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_name", Text),
    Column("password", Text),
)


mapper_registry.map_imperatively(
    Album,
    album_table,
    properties = {
        "artist": relationship(
            Artist,
            back_populates = "artist",
            uselist = False
        ),
        "tracks": relationship(
            Track,
            back_populates="track"
        )
    }
)

mapper_registry.map_imperatively(Artist, artist_table)

mapper_registry.map_imperatively(
    Favourite,
    favourite_table,
    properties = {
        "track": relationship(
            Track,
            back_populates="track",
            uselist = False
        )
    }
)

mapper_registry.map_imperatively(Genre, genre_table)

mapper_registry.map_imperatively(
    Review,
    review_table,
    properties = {
        "track": relationship(
            Track,
            back_populates="track",
            uselist = False
        )
    }
)

mapper_registry.map_imperatively(
    Track,
    track_table,
    properties = {
        "artist": relationship(
            Artist,
            back_populates="artist",
            uselist = False
        ),
        "album": relationship(
            Album,
            back_populates="album",
            uselist = False
        ),
        "genres": relationship(
            Genre,
            back_populates="genre"
        ),
        "reviews": relationship(
            Review,
            back_populates="review"
        )
    }
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties = {
        "reviews": relationship(
            Review,
            back_populates="review"
        ),
        "favourites": relationship(
            Favourite,
            back_populates="favourite"
        )
    }
)
