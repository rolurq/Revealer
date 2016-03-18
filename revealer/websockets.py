from flask.ext.socketio import emit

from . import socketio


@socketio.on('connect')
def test_connect():
    pass


@socketio.on('multiplex statechanged')
def state_changed(data):
#     print("state change: %s" % data['state'])
    emit(data['socketId'], data, broadcast=True)
