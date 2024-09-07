"""
Top-level functional tests for the MCStats application
"""

import os
os.environ['DATABASE_URL'] = 'sqlite://'
#from app import app, db

def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """

    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Marvel Champions Stats' in response.data
    # Test client is not logged in - we should see login link, but no logout
    assert b'login' in response.data
    assert b'logout' not in response.data

def test_home_page_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' (Method Not Allowed) status code is returned
    """

    response = test_client.post('/')
    assert response.status_code == 405
    assert b'Welcome to Marvel Champions Stats' not in response.data
