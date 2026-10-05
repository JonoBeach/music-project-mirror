import os
from typing import override

from sqlalchemy.exc import NoResultFound

from music.adapters.csvdatareader import CSVDataReader
from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.genre import Genre
from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = None

    def __enter__(self):
        self.__session = self.__session_factory()
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None and self.__session is not None:
                self.__session.rollback()
        finally:
            if self.__session is not None:
                self.__session.close()
            self.__session = None

    @property
    def session(self):
        if self.__session is None:
            self.__session = self.__session_factory()
        return self.__session

    def commit(self):
        if self.__session is not None:
            self.__session.commit()

    def rollback(self):
        if self.__session is not None:
            self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = None

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()
            self.__session = None

class DatabaseRepository(AbstractRepository):
    def __init__(self, session_factory, should_populate) -> None:
        self.__session_factory = SessionContextManager(session_factory)
        if should_populate:
            self.load_from_csv()

    def load_from_csv(self):
        data = os.path.join(os.path.dirname(__file__),'data')
        album_file = os.path.join(data, "raw_albums_excerpt.csv")
        track_file = os.path.join(data, "raw_tracks_excerpt.csv")
        reader = CSVDataReader(album_file, track_file)
        reader.read_csv_files()

        with self.__session_factory as session:
            session.add_all(reader.dataset_of_tracks)
            session.add_all(reader.dataset_of_albums)
            session.add_all(reader.dataset_of_artists)
            session.add_all(reader.dataset_of_genres)
            session.commit()

    @override
    def add_track(self, track: Track) -> None:
        with self.__session_factory as session:
            session.merge(track)
            session.commit()

    @override
    def get_track(self, id: int):
        with self.__session_factory as session:
            return session.query(Track).filter(Track.id == id).one_or_none()

    @override
    def add_user(self, user: User) -> None:
        with self.__session_factory as session:
            session.merge(user)
            session.commit()

    @override
    def get_user(self, user_name: str) -> User | None:
        if user_name is None:
            return None
        try:
            with self.__session_factory as session:
                return session.query(User).filter(User.user_name == user_name).one_or_none()
        except NoResultFound:
            print(f"No user found with name: {user_name}")
        return None

    @override
    def add_favourite(self, user: User, favourite: Favourite) -> None:
        if user is None or favourite is None:
            return
        with self.__session_factory as session:
            user.add_favourite(favourite)
            session.merge(user)
            session.commit()

    @override
    def remove_favourite(self, user: User, favourite: Favourite) -> None:
        if user is None or favourite is None:
            return
        with self.__session_factory as session:
            user.remove_favourite(favourite)
            session.merge(user)
            session.commit()

    @override
    def get_user_favourite(self, user: User) -> list:
        if user is None:
            return []
        with self.__session_factory() as session:
            user_in_db = session.query(User).filter(User.user_name == user.user_name).one_or_none()
            if user_in_db:
                return user_in_db.favourites
            else:
                print(f"No user found with name: {user.user_name}")
                return []

    @override
    def add_review(self, user: User, review: Review, track: Track) -> None:
        if user is None or review is None or track is None:
            return
        with self.__session_factory as session:
            user.add_review(review)
            track.add_review(review)
            session.merge(user)
            session.merge(track)
            session.commit()

    @override
    def remove_review(self, user: User, review: Review, track: Track) -> None:
        if user is None or review is None or track is None:
            return
        with self.__session_factory as session:
            user.remove_review(review)
            track.remove_review(review)
            session.merge(user)
            session.merge(track)
            session.commit()

    @override
    def get_review_by_date(self, track: Track) -> list:
        if track is None:
            return []
        with self.__session_factory as session:
            track_in_db = session.query(Track).filter(Track.id == track.id).one_or_none()
            if track_in_db:
                return sorted(track_in_db.reviews, key=lambda review: review.date_submitted)
            else:
                print(f"No track found with id: {track.id}")
                return []

    @override
    def get_review_by_rating(self, track: Track) -> list:
        if track is None:
            return []
        with self.__session_factory as session:
            track_in_db = session.query(Track).filter(Track.id == track.id).one_or_none()
            if track_in_db:
                return sorted(track_in_db.reviews, key=lambda review: review.rating, reverse=True)
            else:
                print(f"No track found with id: {track.id}")
                return []

    @override
    def sort_by_track_title(self) -> list:
        with self.__session_factory as session:
            tracks = session.query(Track).all()
            return sorted(tracks, key=lambda track: track.title)

    @override
    def search_by_title(self, title: str) -> list:
        with self.__session_factory() as session:
            tracks = session.query(Track).filter(Track.title.contains(title)).all()
            return tracks

    @override
    def search_by_genre(self, genre: str) -> list:
        with self.__session_factory as session:
            tracks = session.query(Track).join(Track.genres).filter(Genre.name == genre).all()
            return tracks

    @override
    def search_by_artist(self, artist: str) -> list:
        if artist is None:
            return []
        with self.__session_factory() as session:
            tracks = session.query(Track).join(Track.artist).filter(Artist.full_name.contains(artist)).all()
            return tracks

    @override
    def search_by_album(self, album: str) -> list:
        if album is None:
            return []
        with self.__session_factory as session:
            tracks = session.query(Track).join(Track.album).filter(album.title.contains(album)).all()
            return tracks

    @override
    def get_user_list(self) -> list:
        raise NotImplementedError
