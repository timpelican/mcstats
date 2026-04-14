from app.models import User, Aspect

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

def test_aspect_cell():
    """
    GIVEN an Aspect mnodel
    WHEN the Aspect is asked to render as a cell
    THEN a string including <td> tags and the default colour is returned
    """
    a = Aspect(name='Boring')
    assert a.as_cell() == '<td style="color:#000000; background-color:#ffffff;">Boring</td>'

def test_aspect_span():
    """
    GIVEN an Aspect mnodel
    WHEN the Aspect is asked to render as a span
    THEN a string including <span> tags and the default colour is returned
    """
    a = Aspect(name='Boring')
    assert a.as_span() == '<span style="color:#000000; background-color:#ffffff;">Boring</span>'

def test_aspect_cell_colour():
    """
    GIVEN an Aspect mnodel with the non-default colours
    WHEN the Aspect is asked to render as a cell
    THEN a string including <span> tags and the colour is returned
    """
    a = Aspect(name='Crazy', fg_colour='#ff0000', bg_colour='#00ff00')
    assert a.as_cell() == '<td style="color:#ff0000; background-color:#00ff00;">Crazy</td>'
