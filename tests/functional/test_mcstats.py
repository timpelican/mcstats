"""
Top-level functional tests for the MCStats application
"""

from flask import url_for
from flask_login import current_user

def test_config(test_app):
    """
    GIVEN a Flask application configured for testing
    WHEN the tests start
    THEN the application config is set correctly
    """
    assert test_app.config['TESTING'] is True
    assert test_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://'

def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """

    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Marvel Champions Stats' in response.data
    # Test client is not logged in - we should see login link, but no logout
    assert b'login' in response.data
    assert b'logout' not in response.data

def test_home_page_auth(test_client, test_auth):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/')
        assert response.status_code == 200
        assert b'Marvel Champions Stats' in response.data
        # Test client is not logged in - we should see login link, but no logout
        assert b'login' not in response.data
        assert b'logout' in response.data

def test_home_page_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' (Method Not Allowed) status code is returned
    """

    response = test_client.post('/')
    assert response.status_code == 405
    assert b'Welcome to Marvel Champions Stats' not in response.data

def test_login_anonymous(test_client):
    """
    GIVEN no user session
    WHEN the client tries to login (GET)
    THEN the login form is returned
    """
    with test_client:
        response = test_client.get('/login')
        assert response.status_code == 200
        assert b'Username' in response.data
        assert b'Password' in response.data
        assert b'Remember Me' in response.data

def test_login_user(test_client, test_auth):
    """
    GIVEN a logged in user
    WHEN the client tries to login (GET)
    THEN a redirect to the index is returned
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/login')
        assert response.status_code == 302
        assert response.headers['Location'] == url_for('index')

def test_login_form_pass(test_client, test_auth):
    """
    GIVEN no user session
    WHEN the client tries to login (POST) with the correct credentials
    THEN the session is logged in
    """
    with test_client.application.test_request_context():
        test_auth.create()
        # test_auth.login()
        assert current_user.is_authenticated is False
        response = test_client.post('/login', data={'username': test_auth.username, 'password': test_auth.password})
        assert current_user.is_authenticated is True
        assert response.status_code == 302
        assert response.headers['Location'] == url_for('index')

def test_login_form_fail(test_client, test_auth):
    """
    GIVEN no user session
    WHEN the client tries to login (POST) with the incorrect credentials
    THEN the session is not logged in, and requested to login again
    """
    with test_client.application.test_request_context():
        test_auth.create()
        # test_auth.login()
        assert current_user.is_authenticated is False
        response = test_client.post('/login', data={'username': test_auth.username, 'password': 'BADPASSWORD'})
        assert current_user.is_authenticated is False
        assert response.status_code == 302
        assert response.headers['Location'] == url_for('login')
