from gevent import monkey
monkey.patch_all()
from geventwebsocket.server import WebSocketServer


from presentation import app, socketio
from flask.ext.script import Manager, Shell

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def runserver():
    http_server = WebSocketServer(('127.0.0.1', 5001), app)
    http_server.serve_forever()

if __name__ == '__main__':
    manager.run()
