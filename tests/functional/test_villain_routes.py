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

def test_villain_show(test_client, test_villain):
    """
    GIVEN a Flask application configured for testing
    WHEN the /villain/<x> page is requested (GET)
    THEN details of the villain are returned
    """
    with test_client.application.test_request_context():
        response = test_client.get('/villain/1')
        assert response.status_code == 200
        assert b'Big Bad Bob' in response.data

def test_villain_update_noauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/villain/<x>/update' page is requested (GET)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.get('/villain/1/update')
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_villain_update_auth(test_client, test_auth, test_villain):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/<x>/update' page is requested (GET)
        for a valid Villain ID
    THEN check the form is returned
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/villain/1/update')
        assert response.status_code == 200
        assert b'Villain Name' in response.data

def test_villain_update_auth_bad_id(test_client, test_auth, test_villain):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/<x>/update' page is requested (GET)
        for an invalid Villain ID
    THEN check a redirect to the index is returned
        AND a flash message is provided
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/villain/2/update')
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None 

def test_villain_update_post_noauth(test_client, test_villain):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/villain/<x>/update' page is requested (POST)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.post('/villain/1/update',
                                    data={'name': 'Bigger Badder Bob',
                                          'phase_id': 1})
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_villain_update_post_auth(test_client, test_auth, test_phase, test_villain):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/<x>/update' page is requested (POST)
        for an valid villain ID
    THEN check the form is submitted and the villain updated
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/villain/1/update',
                                    data={'name': 'Bigger Badder Bob',
                                          'phase': 1,
                                          'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('villain') in response.headers['Location']

        # Confirm that villain has been updated

        response = test_client.get('/villain/1')
        assert response.status_code == 200
        assert b'Bigger Badder Bob' in response.data 

def test_villain_update_post_auth_bad_id(test_client, test_auth, test_phase, test_villain):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/<x>/update' page is requested (POST)
        for an invalid villain ID
    THEN check a redirect to the index is returned
        AND a flash message is provided
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/villain/2/update',
                                    data={'name': 'Bigger Badder Bob',
                                          'phase': 1,
                                          'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None 

def test_villain_delete_noauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/villain/<x>/delete' page is requested (GET)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.get('/villain/1/delete')
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_villain_delete_auth(test_client, test_auth, test_villain):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/<x>/delete' page is requested (GET)
        for a valid Villain ID
    THEN check the form is returned
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/villain/1/delete')
        assert response.status_code == 200
        assert b'Confirm' in response.data

def test_villain_delete_auth_bad_id(test_client, test_auth, test_villain):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/<x>/delete' page is requested (GET)
        for an invalid Villain ID
    THEN check a redirect to the index is returned
        AND a flash message is provided
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.get('/villain/2/delete')
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None

def test_villain_delete_post_noauth(test_client, test_villain):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/villain/<x>/delete' page is requested (POST)
    THEN check user is redirected to login
    """
    with test_client.application.test_request_context():
        response = test_client.post('/villain/1/delete',
                                    data={'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('login') in response.headers['Location'] 

def test_villain_delete_post_auth(test_client, test_auth, test_phase, test_villain):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/<x>/delete' page is requested (POST)
        for an valid villain ID
    THEN check the form is submitted and the villain updated
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/villain/1/delete',
                                    data={'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('villain') in response.headers['Location']

        # Confirm that villain has been deleted

        response = test_client.get('/villain/1')
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None

def test_villain_delete_post_auth_bad_id(test_client, test_auth, test_phase, test_villain):
    """
    GIVEN a Flask application configured for testing
        AND a logged-in user
    WHEN the '/villain/<x>/delete' page is requested (POST)
        for an invalid villain ID
    THEN check a redirect to the index is returned
        AND a flash message is provided
    """
    with test_client.application.test_request_context():
        test_auth.create()
        test_auth.login()
        assert current_user.is_authenticated is True
        response = test_client.post('/villain/1/delete',
                                    data={'submit': 'submit'})
        assert response.status_code == 302
        assert url_for('index') in response.headers['Location']
        with test_client.session_transaction() as session:
            assert session['_flashes'] is not None 
