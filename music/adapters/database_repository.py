import os
from typing import override

from music.adapters.csvdatareader import CSVDataReader
from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track

class DatabaseRepository(AbstractRepository):
    def __init__(self, session_factory) -> None:
        self.__session_factory = session_factory
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
        raise NotImplementedError

    @override
    def get_user(self, user_name: str) -> User | None:
        raise NotImplementedError

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
