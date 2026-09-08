from flask import session
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User
from music.domainmodel.favourite import Favourite

from music.adapters.repository import repo_instance


def add_favourite(track: Track, repository: AbstractRepository):
    user = repo_instance.get_user(session['username'])
    id = len(repo_instance.get_user_favourite(user))
    favourite = Favourite(id, user.user_id, track)
    repo_instance.add_favourite(user, favourite)
