import os
from typing import override

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from music.adapters.csvdatareader import CSVDataReader
from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class DatabaseRepository(AbstractRepository):
    def __init__(self, session_factory, should_populate) -> None:
        self.__session_factory = session_factory
        self._session_cm = SessionContextManager(session_factory)

        if should_populate:
            self.load_from_csv()

    def load_from_csv(self):
        data = os.path.join(os.path.dirname(__file__),'data')
        album_file = os.path.join(data, "raw_albums_excerpt.csv")
        track_file = os.path.join(data, "raw_tracks_excerpt.csv")
        reader = CSVDataReader(album_file, track_file)
        reader.read_csv_files()

        with self.__session_factory() as session:
            session.add_all(reader.dataset_of_tracks)
            session.add_all(reader.dataset_of_albums)
            session.add_all(reader.dataset_of_artists)
            session.add_all(reader.dataset_of_genres)
            session.commit()

    @override
    def add_track(self, track: Track) -> None:
        raise NotImplementedError

    @override
    def get_track(self, id:int) -> Track | None:
        raise NotImplementedError

    @override
    def add_user(self, user: User) -> None:
        print(user.id)
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    @override
    def get_user(self, user_name: str) -> User | None:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # if no matching user found in the db
            pass

        return user

    @override
    def add_favourite(self, user: User, favourite: Favourite) -> None:
        raise NotImplementedError

    @override
    def remove_favourite(self, user: User, favourite: Favourite) -> None:
        raise NotImplementedError

    @override
    def get_user_favourite(self, user: User) -> list:
        raise NotImplementedError

    @override
    def add_review(self, user: User, review: Review, track: Track) -> None:
        raise NotImplementedError

    @override
    def remove_review(self, user: User, review: Review, track: Track) -> None:
        raise NotImplementedError

    @override
    def get_review_by_date(self, track: Track) -> list:
        raise NotImplementedError

    @override
    def get_review_by_rating(self, track: Track) -> list:
        raise NotImplementedError

    @override
    def sort_by_track_title(self) -> list:
        raise NotImplementedError

    @override
    def search_by_title(self, title: str) -> list:
        raise NotImplementedError

    @override
    def search_by_genre(self, genre: str) -> list:
        raise NotImplementedError

    @override
    def search_by_artist(self, artist: str) -> list:
        raise NotImplementedError

    @override
    def search_by_album(self, album: str) -> list:
        raise NotImplementedError

    @override
    def get_user_list(self) -> list:
        raise NotImplementedError
