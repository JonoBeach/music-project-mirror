from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry
import music.domainmodel as model

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
    Column("user_id", Integer, ForeignKey("users.id"), nullable = false, unique = True),
)

genre_table = Table(
    "genre",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable = false)
)

review_table = Table(
    "review",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable = false, unique = True),
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
    model.Album,
    album_table,
    properties = {
        "artist": relationship(
            model.Artist,
            back_populates = "artist",
            uselist = False
        ),
        "tracks": relationship(
            model.Track,
            back_populates="track"
        )
    }
)

mapper_registry.map_imperatively(model.Artist, artist_table)

mapper_registry.map_imperatively(
    model.Favourite,
    favourite_table,
    properties = {
        "track": relationship(
            model.Track,
            back_populates="track",
            uselist = False
        )
    }
)

mapper_registry.map_imperatively(model.Genre, genre_table)

mapper_registry.map_imperatively(
    model.Review,
    review_table,
    properties = {
        "track": relationship(
            model.Track,
            back_populates="track",
            uselist = False
        )
    }
)

mapper_registry.map_imperatively(
    model.Track,
    track_table,
    properties = {
        "artist": relationship(
            model.Artist,
            back_populates="artist",
            uselist = False
        ),
        "album": relationship(
            model.Album,
            back_populates="album",
            uselist = False
        ),
        "genres": relationship(
            model.Genre,
            back_populates="genre"
        ),
        "reviews": relationship(
            model.Review,
            back_populates="review"
        )
    }
)

mapper_registry.map_imperatively(
    model.User,
    user_table,
    properties = {
        "reviews": relationship(
            model.Review,
            back_populates="review"
        ),
        "favourites": relationship(
            model.Favourite,
            back_populates="favourite"
        )
    }
)
