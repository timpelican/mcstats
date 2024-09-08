"""
Functional tests for villain routes
"""

from flask import url_for
from flask_login import current_user
import pprint

def test_villain_create_noauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/villain/create' page is requested (GET)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.get('/villain/create')
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_villain_create_auth(test_client, test_auth):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/create' page is requested (GET)
    THEN check the form is returned
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/villain/create')
        assert response.status_code == 200
        assert b'Villain Name' in response.data 

def test_villain_create_post_noauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/villain/create' page is requested (POST)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.post('/villain/create', data={'name': 'Bob', 'phase_id': 1})
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_villain_create_post_auth(test_client, test_auth, test_phase):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/create' page is requested (POST)
    THEN check the form is submitted and the villain created
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/villain/create', data={'name': 'Bob', 'phase': 1, 'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('villain') in response.headers['Location']

        # Confirm that new villain has been created

        response = test_client.get('/villain/1')
        assert response.status_code == 200
        assert b'Bob' in response.data 

def test_villain_list(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/villain' page is requested (GET)
    THEN check a list of villains is returned
    """
    with test_client.application.test_request_context():
        response = test_client.get('/villain')
        assert response.status_code == 200
        assert b'Villains' in response.data
    

# def test_home_page_auth(test_client, test_auth):
#     """
#     GIVEN a Flask application configured for testing
#         AND a logged-in user
#     WHEN the '/' page is requested (GET)
#     THEN check the response is valid
#     """
#     with test_client.application.test_request_context():
#         test_auth.create()
#         test_auth.login()
#         assert current_user.is_authenticated is True
#         response = test_client.get('/')
#         assert response.status_code == 200
#         assert b'Welcome to Marvel Champions Stats' in response.data
#         # Test client is not logged in - we should see login link, but no logout
#         assert b'login' not in response.data
#         assert b'logout' in response.data

# def test_home_page_post(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/' page is posted to (POST)
#     THEN check that a '405' (Method Not Allowed) status code is returned
#     """

#     response = test_client.post('/')
#     assert response.status_code == 405
#     assert b'Welcome to Marvel Champions Stats' not in response.data

# def test_login_anonymous(test_client):
#     """
#     GIVEN no user session
#     WHEN the client tries to login (GET)
#     THEN the login form is returned
#     """
#     with test_client:
#         response = test_client.get('/login')
#         assert response.status_code == 200
#         assert b'Username' in response.data
#         assert b'Password' in response.data
#         assert b'Remember Me' in response.data

# def test_login_user(test_client, test_auth):
#     """
#     GIVEN a logged in user
#     WHEN the client tries to login (GET)
#     THEN a redirect to the index is returned
#     """
#     with test_client.application.test_request_context():
#         test_auth.create()
#         test_auth.login()
#         assert current_user.is_authenticated is True
#         response = test_client.get('/login')
#         assert response.status_code == 302
#         assert response.headers['Location'] == url_for('index')
