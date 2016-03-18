from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    ValidationError
from wtforms.validators import Required, Length, Regexp, EqualTo
from ..models import User


class LoginForm(Form):
    username = StringField('Username', validators=(Required(), Length(1, 80)))
    password = PasswordField('Password', validators=(Required()))
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(Form):
    username = StringField('Username', validators=(Required(), Length(1, 80),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames '
                                  'must have only letters, numbers, dots or '
                                  'underscores')))
    password = PasswordField('Password', validators=(Required(),
                             EqualTo('password_confirm',
                                     message="Passwords must match")))
    password_confirm = PasswordField('Confirm password',
                                     validators=(Required()))
    submit = SubmitField("Register")

    # WTF adds this as validator to username
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')
