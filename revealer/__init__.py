from flask import Flask
from flask.ext.socketio import SocketIO
from flask.ext.uploads import UploadSet, configure_uploads
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')

socketio = SocketIO(app)

slideshows = UploadSet('slideshows', ('html'))
configure_uploads(app, (slideshows))

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

from . import views
from . import websockets
