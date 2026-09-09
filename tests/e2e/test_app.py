import pytest

from flask import session
from werkzeug.wrappers import response
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


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, username='test', password='Test1234', confirm='Test1234'):
        # need to register a user to login properly
        self.__client.post(
            '/authentication/register',
            data={'username': 'test', 'password': 'Test1234', 'confirm': 'Test1234'}
        )

        return self.__client.post(
            '/authentication/login',
            data={'username': username, 'password': password, 'confirm': confirm}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def authentication(client):
    return AuthenticationManager(client)


class TestAuthentication:
    def test_register(self, client):
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

    def test_register_with_invalid_input(self, client, username, password, confirm, message):
        # checking that all the password & username requirements are met, and the messages are correct
        if username == 'duplicate':
            client.post('/authentication/register', data={'username': 'duplicate', 'password': 'Test1234', 'confirm': 'Test1234'})

        response = client.post(
            '/authentication/register',
            data={'username': username, 'password': password, 'confirm': confirm},
        )
        assert message in response.data


    def test_login(self, client, authentication):
        # get login page
        status_code = client.get('/authentication/login').status_code
        assert status_code == 200

        # checking that successful login redirects to home page
        response = authentication.login()
        print(response.data)
        assert response.status_code == 302
        assert response.headers['Location'] == '/'

        # check that logging in creates a session for the user
        with client:
            client.get('/')
            assert session['username'] == 'test'


    def test_logout(self, client, authentication):
        authentication.login()

        with client:
            # checking that logging out clears user session
            authentication.logout()
            assert 'username' not in session

class TestBrowseFunctionality:
    def test_browse_tracks(self, client):
        response = client.get('/browse_tracks')
        assert response.status_code == 200


    def test_browse_tracks_pagination(self, client):
        response = client.get('/browse_tracks?page=1')
        assert response.status_code == 200

        response = client.get('/browse_tracks?page=3')
        assert response.status_code == 200

        #test page out of range and invalid value
        response = client.get('/browse_tracks?page=-1')
        assert response.status_code == 200

        response = client.get('/browse_tracks?page=999')
        assert response.status_code == 200

        response = client.get('/browse_tracks?page=abcd')
        assert response.status_code == 200


    def test_search_tracks(self, client):
        #test search by title
        response = client.get('/browse_tracks?search=a&search_type=title')
        assert response.status_code == 200

        #test search by artist
        response = client.get('/browse_tracks?search=a&search_type=artist')
        assert response.status_code == 200

        #test search by album
        response = client.get('/browse_tracks?search=a&search_type=album')
        assert response.status_code == 200

        #test notfound case. should return 200
        response = client.get('/browse_tracks?search=abcdefg&search_type=title')
        assert response.status_code == 200


    def test_track_detail(self, client):
        # test valid track
        response = client.get('/track/5')
        assert response.status_code == 200

        #test not exist track
        response = client.get('/track/9999')
        assert response.status_code == 404

        #test invalid value
        response = client.get('/track/abc')
        assert response.status_code == 404


class TestFavouriteFunctionality:
    def test_add_favourite_from_browse_tracks(self, client, authentication):
        authentication.login()
        client.post('/browse_tracks', data={'action': 'Add to favourites', 'track_id': '1249'})
        response = client.get('/favourites')
        assert b'Metal Laquer' in response.data


    def test_add_favourite_from_track_details(self, client, authentication):
        authentication.login()
        client.post('/track/1249', data={'action': 'Add to favourites', 'track_id': '1249'})
        response = client.get('/favourites')
        assert b'Metal Laquer' in response.data


    def test_logged_out_add_favourite_from_browse_tracks(self, client, authentication):
        response = client.post('/browse_tracks', data={'action': 'Add to favourites', 'track_id': '1249'})
        assert response.headers['Location'] == '/authentication/login'


    def test_logged_out_add_favourite_from_track_details(self, client, authentication):
        response = client.post('/track/1249', data={'action': 'Add to favourites', 'track_id': '1249'})
        assert response.headers['Location'] == '/authentication/login'


    def test_remove_favourite_from_browse_tracks(self, client, authentication):
        # first add favourite
        authentication.login()
        client.post('/browse_tracks', data={'action': 'Add to favourites', 'track_id': '1249'})
        response = client.get('/favourites')
        assert b'Metal Laquer' in response.data

        # remove
        client.post('/browse_tracks', data={'action': 'Remove from favourites', 'track_id': '1249'})
        response = client.get('/favourites')
        assert b'Metal Laquer' not in response.data


    def test_remove_favourite_from_favourites(self, client, authentication):
        # first add favourite
        authentication.login()
        client.post('/browse_tracks', data={'action': 'Add to favourites', 'track_id': '1249'})
        response = client.get('/favourites')
        assert b'Metal Laquer' in response.data

        # remove
        client.post('/browse_tracks', data={'action': 'Remove from favourites', 'track_id': '1249'})
        response = client.get('/favourites')
        assert b'Metal Laquer' not in response.data


    def test_remove_favourite_from_track_details(self, client, authentication):
        # first add favourite
        authentication.login()
        client.post('/browse_tracks', data={'action': 'Add to favourites', 'track_id': '1249'})
        response = client.get('/favourites')
        assert b'Metal Laquer' in response.data

        # remove
        client.post('/track/1249', data={'action': 'Remove from favourites', 'track_id': '1249'})
        response = client.get('/favourites')
        assert b'Metal Laquer' not in response.data


class TestReviewFunctionality:
    def test_add_review_from_track_details(self, client, authentication):
        authentication.login()
        review = 'this track is really good'
        response = client.post('/track/1249', data={'action': 'Add review', 'rating': '5', 'review': review})
        assert review.encode() in response.data
