import abc

from music.domainmodel.favourite import Favourite
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
        raise NotImplementedError

    @abc.abstractmethod
    def add_favourite(self,user: User, favourite: Favourite) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favourite(self, user: User, favourite: Favourite) -> None:
        raise NotImplementedError
