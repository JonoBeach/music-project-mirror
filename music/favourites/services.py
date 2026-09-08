from flask import session
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User
from music.domainmodel.favourite import Favourite
from music.adapters import repository


def add_favourite(track: Track):
    user = repository.repo_instance.get_user(session['username'])
    id = len(repository.repo_instance.get_user_favourite(user))
    favourite = Favourite(id, user.user_id, track)
    repository.repo_instance.add_favourite(user, favourite)

def remove_favourite(user: User, favourite: favourite):
    repository.repo_instance.remove_favourite(user, favourite)
