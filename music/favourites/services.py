import uuid
from flask import session
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User
from music.domainmodel.favourite import Favourite
from music.adapters import repository

import time

def add_favourite(user: User, track: Track):
    if not any(favourite.track.id == track.id for favourite in user.favourites):
        id = uuid.uuid4().int
        favourite = Favourite(id, user.id, track)
        repository.repo_instance.add_favourite(user, favourite)

def remove_favourite(user: User, favourite: Favourite):
    repository.repo_instance.remove_favourite(user, favourite)
