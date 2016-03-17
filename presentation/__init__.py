from flask import Flask
from flask.ext.socketio import SocketIO

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')

socketio = SocketIO(app)

from flask.ext.uploads import UploadSet, configure_uploads

slideshows = UploadSet('slideshows', ('html'))
configure_uploads(app, (slideshows))

from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.init_app(app)

from auth import auth
app.register_blueprint(auth)

from . import views
from . import websockets
