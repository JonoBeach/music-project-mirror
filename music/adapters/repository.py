import abc

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.favourite import Favourite
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User
#This interface should define the necessary methods for fetching, storing, and
#manipulating data about tracks.


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_track(self, track: Track) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, id:int) -> Track | None:
        #get track by track id
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name:str) -> User | None:
        #get user by user name
        raise NotImplementedError

    @abc.abstractmethod
    def add_favourite(self,user: User, favourite: Favourite) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favourite(self, user: User, favourite: Favourite) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, user: User, review: Review, track: Track) -> None:
        #user add a review to a track
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_by_date(self) -> list:
        #return reviews list sorted by date.(most recently)
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_by_rating(self) -> list:
        #return reviews list sorted by their rating.(high to low)
        raise NotImplementedError

    @abc.abstractmethod
    def alpha_sort_track(self) -> list:
        #return alphabetically sorted track list
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_titile(self, title: str) -> Track | None:
        #return track that have same title or None
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_genre(self, genre: Genre) -> list | None:
        #return a list of track that have same genre or None
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_artist(self, artist: Artist) -> list | None:
        #return a list of track that have same artist or None
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_album(self, album: Album) -> list | None:
        #return a list of track that have same album name or None
        raise NotImplementedError
