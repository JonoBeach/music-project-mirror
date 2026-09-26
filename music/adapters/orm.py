from sqlalchemy import Table, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import registry, relationship
from music.domainmodel import Album, Artist, Favourite, Genre, Review, Track, User

mapper_registry = registry()

album_table = Table(
    "album",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("title", Text),
    Column("artist_id", Integer, ForeignKey("artist.id")),
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
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("track_id", Integer, ForeignKey("track.id"))
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
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("track_id", Integer, ForeignKey("track.id")),
    Column("rating", Integer),
    Column("review_text", Text),
    Column("date_submitted", Integer)
)

track_table = Table(
    "track",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("title", Text),
    Column("artist_id", Integer, ForeignKey("artist.id")),
    Column("album_id", Integer, ForeignKey("album.id")),
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

track_genre_table = Table(
    "track_genre",
    mapper_registry.metadata,
    Column("track_id", Integer, ForeignKey("track.id")),
    Column("genre_id", Integer, ForeignKey("genre.id")),
)


mapper_registry.map_imperatively(Album, album_table,
    properties = {
        "_Album__id": album_table.c.id,
        "_Album__title": album_table.c.title,
        "_Album__release_year": album_table.c.release_year,
        "_Album__artist": relationship(
            Artist,
            uselist = False
        ),
        "_Album__tracks": relationship(
            Track,
            back_populates="_Track__album"
        ),
        "_Album__album_url": album_table.c.album_url,
        "_Album__album_info": album_table.c.album_info
    }
)

mapper_registry.map_imperatively(Artist, artist_table,
    properties = {
        "_Artist__id": artist_table.c.id,
        "_Artist__full_name": artist_table.c.full_name
    }
)

mapper_registry.map_imperatively(Favourite, favourite_table,
    properties = {
        "_Favourite__id": favourite_table.c.id,
        "_Favourite__user_id": favourite_table.c.user_id,
        "_Favourite__track": relationship(
            Track,
            uselist = False
        )
    }
)

mapper_registry.map_imperatively(Genre, genre_table,
    properties = {
        "_Genre__id": genre_table.c.id,
        "_Genre__name": genre_table.c.name
    }
)

mapper_registry.map_imperatively(Review, review_table,
    properties = {
        "_Review__id": review_table.c.id,
        "_Review__user_id": review_table.c.user_id,
        "_Review__track": relationship(
            Track,
            uselist = False
        ),
        "_Review__rating": review_table.c.rating,
        "_Review__review_text": review_table.c.review_text,
        "_Review__date_submitted": review_table.c.date_submitted
    }
)

mapper_registry.map_imperatively(Track, track_table,
    properties = {
        "_Track__id": track_table.c.id,
        "_Track__title": track_table.c.title,
        "_Track__artist": relationship(
            Artist,
            uselist = False
        ),
        "_Track__album": relationship(
            Album,
            back_populates="_Album__tracks",
            uselist = False
        ),
        "_Track__track_url": track_table.c.track_url,
        "_Track__track_duration": track_table.c.track_duration,
        "_Track__genres": relationship(
            Genre,
            secondary=track_genre_table
        ),
        "_Track__reviews": relationship(
            Review
        )
    }
)

mapper_registry.map_imperatively(User, user_table,
    properties = {
        "_User__id": user_table.c.id,
        "_User__user_name": user_table.c.user_name,
        "_User__password": user_table.c.password,
        "_User__reviews": relationship(
            Review
        ),
        "_User__favourites": relationship(
            Favourite
        )
    }
)
