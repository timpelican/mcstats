import os
os.environ['DATABASE_URL'] = 'sqlite://'
from app import app, db
import pytest

@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    # This doesn't quite work right when not using a factory - update later
    # Currently has the in-memory DB set up the top
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!