import os
from typing import override

from music.adapters.csvdatareader import CSVDataReader
from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track

class MemoryRepository(AbstractRepository):
    def __init__(self) -> None:
        self.__tracks = list()
        self.__users = list()
        self.__albums = list()
        self.__artists = list()
        self.__genres = list()
        self.load_from_csv()

    def load_from_csv(self):
        data = os.path.join(os.path.dirname(__file__),'data')
        album_file = os.path.join(data, "raw_albums_excerpt.csv")
        track_file = os.path.join(data, "raw_tracks_excerpt.csv")

        reader = CSVDataReader(album_file, track_file)
        reader.read_csv_files()

        self.__tracks = reader.dataset_of_tracks
        self.__albums = reader.dataset_of_albums
        self.__artists = reader.dataset_of_artists
        self.__genres = reader.dataset_of_genres

    @override
    def add_track(self, track: Track) -> None:
        self.__tracks.append(track)

    @override
    def get_track(self, id:int) -> Track | None:
        return next((track for track in self.__tracks if track.track_id == id), None)

    @override
    def add_user(self, user: User) -> None:
        self.__users.append(user)

    @override
    def get_user(self, user_name: str) -> User | None:
        return next((user for user in self.__users if user.user_name == user_name), None)

    @override
    def add_favourite(self, user: User, favourite: Favourite) -> None:
        for favou in self.get_user_favourite(user):
            if favou.track == favourite.track:
                return
        user.add_favourite(favourite)

    @override
    def remove_favourite(self, user: User, favourite: Favourite) -> None:
        user.remove_favourite(favourite)

    @override
    def get_user_favourite(self, user: User) -> list:
        return user.favourites

    @override
    def add_review(self, user: User, review: Review, track: Track) -> None:
        user.add_review(review)
        track.add_review(review)

    @override
    def remove_review(self, user: User, review: Review, track: Track) -> None:
        user.remove_review(review)
        track.remove_review(review)

    @override
    def get_review_by_date(self, track: Track) -> list:
        list = track.reviews
        for i in range(len(list)):
            for j in range(0, len(list) - i - 1):
                if list[j].date_submitted > list[j + 1].date_submitted:
                    temp = list[j]
                    list[j] = list[j + 1]
                    list[j + 1] = temp
        return list

    @override
    def get_review_by_rating(self, track: Track) -> list:
        list = track.reviews
        for i in range(len(list)):
            for j in range(0, len(list) - i - 1):
                if list[j].rating < list[j + 1].rating:
                    temp = list[j]
                    list[j] = list[j + 1]
                    list[j + 1] = temp
        return list
