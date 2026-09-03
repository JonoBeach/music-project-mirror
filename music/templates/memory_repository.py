import os
from typing import override

from music.adapters.csvdatareader import CSVDataReader
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User
from music.templates.repository import AbstractRepository
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
        data = os.path.join(os.path.dirname(__file__), '..', 'adapters', 'data')
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
        user.add_favourite(favourite)

    @override
    def remove_favourite(self, user: User, favourite: Favourite) -> None:
        user.remove_favourite(favourite)
