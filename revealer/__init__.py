from flask import Flask
from flask.ext.socketio import SocketIO
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.admin import Admin

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')

socketio = SocketIO(app, async_mode='gevent')

slideshows = UploadSet('slideshows', ('html'))
resources = UploadSet('resources', ('css', 'js') + IMAGES)
configure_uploads(app, (slideshows, resources))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'success'

db = SQLAlchemy()
db.init_app(app)

bootstrap = Bootstrap(app)

moment = Moment(app)

from auth import auth
from slides import slides

app.register_blueprint(auth)
app.register_blueprint(slides)

from admin.models import UserAdmin, SlideshowAdmin
from .models import User, Slideshow

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(UserAdmin(User, db.session))
admin.add_view(SlideshowAdmin(Slideshow, db.session))

from . import views
