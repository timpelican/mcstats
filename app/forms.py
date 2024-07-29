from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class VillainForm(FlaskForm):
    name = StringField('Villain Name', validators=[DataRequired()])
    phase = RadioField('Phase', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit')

class HeroForm(FlaskForm):
    name = StringField('Hero Name', validators=[DataRequired()])
    phase = RadioField('Phase', validators=[DataRequired()], coerce=int)
    aspect = SelectField('Default Aspect', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit')