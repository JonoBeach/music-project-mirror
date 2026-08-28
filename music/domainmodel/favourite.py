from music.domainmodel.user import User
from music.domainmodel.track import Track

class Favourite:
    # TODO: Complete the implementation of the Favourite class.
    def __init__(self, id: int, user: User, track: Track):

        if type(id) is not int:
            raise ValueError("Favourite ID should be an integer.")
        self.__id = id

        if not isinstance(user, User):
            raise ValueError("user must be a User instance.")
        self.__user = user

        if not isinstance(track, Track):
            raise ValueError("track must be a Track instance.")
        self.__track = track

    @property
    def id(self) -> int:
        return self.__id

    @property
    def user(self) -> User:
        return self.__user

    @property
    def track(self) -> Track:
        return self.__track

    def __repr__(self) -> str:
        return f'<Favourite {self.id}, user = {self.user.user_name}, track = {self.track.title}>'

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return self.id == value.id

    def __lt__(self, value):
        if not isinstance(value, self.__class__):
            return True
        return self.id < value.id

    def __hash__(self) -> int:
        return hash(self.id)