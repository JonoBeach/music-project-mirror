import uuid
import random
from flask import session
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User
from music.domainmodel.favourite import Favourite
from music.adapters import repository

import time

def add_favourite(user: User, track: Track):
    if not any(favourite.track.id == track.id for favourite in user.favourites):
        # id = int(str(uuid.uuid4().int)[:15])
        id = random.randint(0, 10000000)
        favourite = Favourite(id, user.id, track)
        print("added favourite: ", favourite.track.title)
        repository.repo_instance.add_favourite(user, favourite)

def remove_favourite(user: User, favourite: Favourite):
    repository.repo_instance.remove_favourite(user, favourite)
