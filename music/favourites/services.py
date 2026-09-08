from flask import session
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User
from music.domainmodel.favourite import Favourite


def add_favourite(track: Track, repository: AbstractRepository):
    user = repository.get_user(session['username'])
    id = len(repository.get_user_favourite(user))
    favourite = Favourite(id, user.user_id, track)
    repository.add_favourite(user, favourite)
