import abc

from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User
#This interface should define the necessary methods for fetching, storing, and
#manipulating data about tracks.

repo_instance: AbstractRepository | None = None

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
    def get_user_favourites(self, user: User) -> list:
        #return a list of favourite that belong to the user
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, user: User, review: Review, track: Track) -> None:
        #user add a review to a track
        raise NotImplementedError

    @abc.abstractmethod
    def remove_review(self, user: User, review: Review, track: Track) -> None:
        #delete a review
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_by_date(self, track: Track) -> list:
        #return reviews list sorted by date.(most recently)
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_by_rating(self, track: Track) -> list:
        #return reviews list sorted by their rating.(high to low)
        raise NotImplementedError

    @abc.abstractmethod
    def sort_by_track_title(self) -> list:
        #return alphabetically sorted track list
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_title(self, title: str) -> list:
        #return track list that partial match on same str in parameter
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_genre(self, genre: str) -> list:
        #return a list of track that partial match same str
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_artist(self, artist: str) -> list:
        #return a list of track that partial match same str
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_album(self, album: str) -> list:
        #return a list of track that partial match same str
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_list(self) -> list:
        # returns the full list of user objects, for registering new users to get an ID
        raise NotImplementedError
