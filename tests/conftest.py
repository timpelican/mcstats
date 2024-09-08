"""
Fixtures for tests
"""
import os
os.environ['DATABASE_URL'] = 'sqlite://'
import pytest
import sqlalchemy as sa
from flask_login import login_user, logout_user
from app import app, db
from app.models import User

class AuthActions():
    """
    Helpers for testing authenticated user without using the /login route
    Testers don't need to know a valid user name and password, it's all self-contained
    """
    def __init__(self, client, username='TestUser', password='TestPass', email='test@example.com'):
        """
        Create the helper
        """
        self.client = client
        self.username = username
        self.password = password
        self.email = email

    def create(self):
        """
        Create the user in the DB
        """
        with self.client.application.app_context():
            test_user = User(username=self.username, email=self.email)
            test_user.set_password(self.password)
            db.session.add(test_user)
            db.session.commit()

    def login(self):
        """
        Login with the created user
        """
        with self.client.application.app_context():
            user = db.session.scalar(
                sa.select(User).where(User.username == self.username))
            return login_user(user)

    def logout(self):
        """
        Logout the user
        """
        return logout_user()

@pytest.fixture()
def test_app():
    """
    App fixture - overrides to in-memory DB and creates all tables
    """
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://'
    })
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield app

    # Clean up the DB afterwards
    db.drop_all()
    app_context.pop()

@pytest.fixture()
def test_client(test_app):
    """
    Client fixture
    """
    return test_app.test_client()

@pytest.fixture
def test_auth(test_client):
    """
    Authenticated client fixture
    """
    return AuthActions(test_client)
