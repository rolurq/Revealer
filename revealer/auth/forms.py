# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    ValidationError
from wtforms.validators import Required, Length, Regexp, EqualTo, Optional,\
    Email
from ..models import User


class LoginForm(Form):
    username = StringField('Login', validators=(Required(), Length(1, 32)))
    password = PasswordField('Password', validators=(Required(),))
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

    def validate_username(self, field):
        if not self.get_user():
            raise ValidationError('Invalid username')

    def validate_password(self, field):
        user = self.get_user()
        if user and not user.verify_password(field.data):
            raise ValidationError('Invalid password')

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()


class RegistrationForm(Form):
    name = StringField('Name', validators=(Length(0, 64), Optional(),
                       Regexp('^[A-ZÁÉÍÓÚÑa-záéíóúñ\s]*$', 0, 'Names must have'
                              ' only letters and spaces')),
                       description="Your full name")
    username = StringField('Login', validators=(Required(), Length(1, 32),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames '
                                  'must have only letters, numbers, dots or '
                                  'underscores')))
    email = StringField('Email', validators=(Optional(), Length(0, 64),
                                             Email()))
    password = PasswordField('Password', validators=(Required(),
                             EqualTo('password_confirm',
                                     message="Passwords must match")))
    password_confirm = PasswordField('Confirm password',
                                     validators=(Required(),))
    submit = SubmitField("Register")

    # WTF adds this as validator to username
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')


class EditProfileForm(Form):
    name = StringField('Name', validators=(Length(0, 64), Optional(),
                       Regexp('^[A-ZÁÉÍÓÚÑa-záéíóúñ\s]*$', 0, 'Names must have'
                              ' only letters and spaces')),
                       description="Your full name")
    username = StringField('Login', validators=(Length(0, 32), Optional(),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames '
                                  'must have only letters, numbers, dots or '
                                  'underscores')))
    submit = SubmitField("Save Changes")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and\
           User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')
