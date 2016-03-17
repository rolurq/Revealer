from flask import Flask
from flask.ext.socketio import SocketIO
from flask.ext.uploads import UploadSet, configure_uploads
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap

from auth import auth

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')

socketio = SocketIO(app)

slideshows = UploadSet('slideshows', ('html'))
configure_uploads(app, (slideshows))

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy()
db.init_app(app)

bootstrap = Bootstrap(app)

app.register_blueprint(auth)

from . import views
from . import websockets
