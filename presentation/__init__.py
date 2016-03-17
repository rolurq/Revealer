from flask import Flask
from flask.ext.socketio import SocketIO

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')

socketio = SocketIO(app)

from flask.ext.uploads import UploadSet, configure_uploads

slideshows = UploadSet('slideshows', ('html'))
configure_uploads(app, (slideshows))

from auth import auth
app.register_blueprint(auth)

from . import views
from . import websockets
