import os
from typing import override

from music.adapters.csvdatareader import CSVDataReader
from music.domainmodel import track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.favourite import Favourite
from music.domainmodel.genre import Genre
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
        user_name = user_name.lower()
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
        return sorted(track.reviews, key=lambda review: review.date_submitted)

    @override
    def get_review_by_rating(self, track: Track) -> list:
        return sorted(track.reviews, key=lambda review: review.rating, reverse=True)

    @override
    def sort_by_track_title(self) -> list:
        return sorted(self.__tracks, key=lambda track: track.title)

    @override
    def search_by_title(self, title: str) -> Track | None:
        return next((track for track in self.__tracks if track.title == title), None)

    @override
    def search_by_genre(self, genre: Genre) -> list:
        return [track for track in self.__tracks if genre in track.genres]

    @override
    def search_by_artist(self, artist: Artist) -> list:
        return [track for track in self.__tracks if track.artist == artist]

    @override
    def search_by_album(self, album: Album) -> list:
        return [track for track in self.__tracks if track.album == album]

    @override
    def get_user_list(self) -> list:
        return self.__users
