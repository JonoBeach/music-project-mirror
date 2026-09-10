import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class UsernameAlreadyTakenException(Exception):
    pass


def add_user(username: str, password: str, repository: AbstractRepository):
    # check if username is already taken
    user = repository.get_user(username)
    if user is not None:
        raise UsernameAlreadyTakenException

    # encrypt password into hash
    password_hash = generate_password_hash(password)

    id = uuid.uuid4().int
    user = User(id, username, password_hash)
    repository.add_user(user)


def get_user(username: str, repository: AbstractRepository):
    user = repository.get_user(username)
    if user is None:
        raise UnknownUserException

    return get_user_as_dictionary(user)


def authenticate_user(username: str, password: str, repository: AbstractRepository):
    authenticated = False

    user = repository.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def get_user_as_dictionary(user: User):
    user_dict = {
        'username': user.user_name,
        'password': user.password
    }
    return user_dict
