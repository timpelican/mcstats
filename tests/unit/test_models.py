from app.models import User

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email and password_hash are defined correctly
    """
    u = User(username='bob', email='bob@example.com')
    assert u.username == 'bob'
    assert u.email == 'bob@example.com'
    u.set_password('bob123')
    assert u.password_hash != 'bob123'
    assert u.check_password('bob123') is True
    assert u.check_password('fred456') is False