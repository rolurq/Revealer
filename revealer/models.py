from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.event import listens_for
from os import remove as rm
from . import db, login_manager, slideshows, socketio


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.id == 1

    def __repr__(self):
        return self.username


class Slideshow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    last_presented = db.Column(db.DateTime())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('slideshows', lazy='dynamic'))

    def __init__(self, title, user, description):
        self.title = title
        self.user = user
        self.description = description

    def __repr__(self):
        return self.title

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def present(self):
        self.last_presented = datetime.utcnow()
        db.session.add(self)


@listens_for(Slideshow, 'after_delete')
def delete_slideshow(mapper, connection, target):
    try:
        rm(slideshows.path(str(target.id)))
    except OSError:
        pass


# A slideshow being presented
class Presentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slideshow_hash = db.Column(db.String(12), unique=True, index=True)
    clients = db.Column(db.Integer)
    state = db.Column(db.PickleType())
    created = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    slideshow_id = db.Column(db.Integer, db.ForeignKey('slideshow.id'))
    slideshow = db.relationship('Slideshow',
                                backref=db.backref('presentations',
                                                   lazy='dynamic'))

    def __init__(self, slideshow, slideshow_hash):
        self.slideshow = slideshow
        self.slideshow_hash = slideshow_hash

    def connected(self):
        if not self.clients:
            self.clients = 0
        self.clients += 1
        db.session.add(self)

    def disconnected(self):
        self.clients -= 1
        db.session.add(self)

    def statechanged(self, state):
        self.state = state
        db.session.add(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


@listens_for(Presentation, 'after_delete')
def delete_presentation(mapper, connection, target):
    try:
        del socketio.server.handlers['/%s' % target.slideshow_hash]
    except KeyError:
        pass
