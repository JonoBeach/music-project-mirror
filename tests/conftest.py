import pytest

from music import create_app
from music.adapters import memory_repository

from pathlib import Path

# the csv files in the test folder are different from the csv files in the music/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = Path(__file__).parent / "tests" / "data"

@pytest.fixture
def in_memory_repo():
    repo = memory_repository.MemoryRepository()
    database_mode = False
    return repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()

@pytest.fixture
def authentication(client):
    return AuthenticationManager(client)

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, username='test', password='Test1234'):
        self.__client.post(
            'authentication/register',
            data={'username': username, 'password': password, 'confirm': password}
        )
        return self.__client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
