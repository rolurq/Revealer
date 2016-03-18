import eventlet
eventlet.monkey_patch()

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
    socketio.run(app, host='127.0.0.1', port=5001)
if __name__ == '__main__':
    manager.run()
