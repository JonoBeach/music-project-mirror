import os
from typing import override

from music.adapters.csvdatareader import CSVDataReader
from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track

class DatabaseRepository(AbstractRepository):
    def __init__(self) -> None:
        load_from_csv()

    def load_from_csv(self):
        raise NotImplementedError

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
