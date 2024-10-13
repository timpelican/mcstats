"""
Functional tests for hero routes
"""

from flask import url_for
from flask_login import current_user
import pprint

def test_hero_create_noauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hero/create' page is requested (GET)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.get('/hero/create')
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_hero_create_auth(test_client, test_auth):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/create' page is requested (GET)
    THEN check the form is returned
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/hero/create')
        assert response.status_code == 200
        assert b'Hero Name' in response.data

def test_hero_create_post_noauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hero/create' page is requested (POST)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.post('/hero/create', data={'name': 'Bob', 'phase_id': 1, 'aspect_id': 1})
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_hero_create_post_auth(test_client, test_auth, test_phase, test_aspect):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/create' page is requested (POST)
    THEN check the form is submitted and the hero created
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/hero/create', data={'name': 'Safety Queen', 'phase': 1, 'aspect': 1, 'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('hero') in response.headers['Location']

        # Confirm that new hero has been created

        response = test_client.get('/hero/1')
        assert response.status_code == 200
        assert b'Safety Queen' in response.data 

def test_hero_list(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hero' page is requested (GET)
    THEN check a list of heroes is returned
    """
    with test_client.application.test_request_context():
        response = test_client.get('/hero')
        assert response.status_code == 200
        assert b'Heroes' in response.data

def test_hero_show(test_client, test_aspect, test_hero):
    """
    GIVEN a Flask application configured for testing
    WHEN the /hero/<x> page is requested (GET)
    THEN details of the hero are returned
    """
    with test_client.application.test_request_context():
        response = test_client.get('/hero/1')
        assert response.status_code == 200
        assert b'Safety Queen' in response.data

def test_hero_update_noauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hero/<x>/update' page is requested (GET)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.get('/hero/1/update')
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_hero_update_auth(test_client, test_auth, test_aspect, test_hero):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/<x>/update' page is requested (GET)
        for a valid Hero ID
    THEN check the form is returned
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/hero/1/update')
        assert response.status_code == 200
        assert b'Hero Name' in response.data

def test_hero_update_auth_bad_id(test_client, test_auth, test_aspect, test_hero):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/<x>/update' page is requested (GET)
        for an invalid Hero ID
    THEN check a redirect to the index is returned
        AND a flash message is provided
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/hero/2/update')
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None 

def test_hero_update_post_noauth(test_client, test_aspect, test_hero):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hero/<x>/update' page is requested (POST)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.post('/hero/1/update',
                                    data={'name': 'Dairy Queen',
                                          'phase_id': 1})
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_hero_update_post_auth(test_client, test_auth, test_phase, test_aspect, test_hero):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/<x>/update' page is requested (POST)
        for an valid hero ID
    THEN check the form is submitted and the hero updated
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/hero/1/update',
                                    data={'name': 'Dairy Queen',
                                          'phase': 1,
                                            'aspect': 1,
                                          'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('hero') in response.headers['Location']

        # Confirm that hero has been updated

        response = test_client.get('/hero/1')
        assert response.status_code == 200
        assert b'Dairy Queen' in response.data 

def test_hero_update_post_auth_bad_id(test_client, test_auth, test_phase, test_aspect, test_hero):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/<x>/update' page is requested (POST)
        for an invalid Hero ID
    THEN check a redirect to the index is returned
        AND a flash message is provided
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/hero/2/update',
                                    data={'name': 'Dairy Queen',
                                          'phase': 1,
                                          'aspect': 1,
                                          'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None 

def test_hero_delete_noauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hero/<x>/delete' page is requested (GET)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.get('/hero/1/delete')
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_hero_delete_auth(test_client, test_auth, test_hero):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/<x>/delete' page is requested (GET)
        for a valid Hero ID
    THEN check the form is returned
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/hero/1/delete')
        assert response.status_code == 200
        assert b'Confirm' in response.data

def test_hero_delete_auth_bad_id(test_client, test_auth, test_hero):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/<x>/delete' page is requested (GET)
        for an invalid Hero ID
    THEN check a redirect to the index is returned
        AND a flash message is provided
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/hero/2/delete')
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None

def test_hero_delete_post_noauth(test_client, test_hero):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hero/<x>/delete' page is requested (POST)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.post('/hero/1/delete',
                                    data={'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_hero_delete_post_auth(test_client, test_auth, test_phase, test_hero):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/<x>/delete' page is requested (POST)
        for an valid Hero ID
    THEN check the form is submitted and the hero updated
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/hero/1/delete',
                                    data={'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('hero') in response.headers['Location']

        # Confirm that hero has been deleted

        response = test_client.get('/hero/1')
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None

def test_hero_delete_post_auth_bad_id(test_client, test_auth, test_phase, test_hero):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/hero/<x>/delete' page is requested (POST)
        for an invalid Hero ID
    THEN check a redirect to the index is returned
        AND a flash message is provided
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/hero/2/delete',
                                    data={'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None 
