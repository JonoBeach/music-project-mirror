import pytest

from flask import session
from music import create_app

from pathlib import Path

TEST_DATA_PATH = Path(__file__).parent / "tests" / "data"

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False # since test client won't send a CSRF token, disable for testing
    })

    return app.test_client()


def test_register(client):
    # check that we can access the page
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # checking that we can register a user successfully
    response = client.post(
        '/authentication/register',
      data={'username': 'test', 'password': 'Test1234', 'confirm': 'Test1234'}
    )
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'confirm', 'message'), (
        ('', '', '', b'Please input a username!'),
        ('te', '', '', b'Your username is too short!'),
        ('test', '', '', b'Please enter a password'),
        ('test', 'test', '', b'Your password must be at least 8 characters, contain no spaces, contain an upper-case, lower-case, and a digit!'),
        ('test', 'Te st1234', '', b'Your password must be at least 8 characters, contain no spaces, contain an upper-case, lower-case, and a digit!'),
        ('test', 'Test1234', 'Different1234', b'Your password confirmation did not match!'),
        ('duplicate', 'Test1234', 'Test1234', b'This username has already been taken, please choose another'),
))
def test_register_with_invalid_input(client, username, password, confirm, message):
    # checking that all the password & username requirements are met, and the messages are correct

    if username == 'duplicate':
        client.post('/authentication/register', data={'username': 'duplicate', 'password': 'Test1234', 'confirm': 'Test1234'})

    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password, 'confirm': confirm},
    )
    assert message in response.data
