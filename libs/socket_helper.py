import socketio
import eventlet
import eventlet.wsgi
import json

"""
The Socket IO server that will wrap the Flask app and provide Websocket
functionality.
"""
sio = socketio.Server()

"""
Functions to be executed (as fn(messageData)) whenever we receive a message.
"""
message_subscribers = []

"""
Functions to be executed (as fn(connectionId)) whenever a client connects to
the websocket.
"""
connect_subscribers = []

"""
Functions to be executed (as fn(connectionId)) whenever a client disconnects
from the websocket.
"""
disconnect_subscribers = []

def create_socket_server(
        app,
        port,
        connect_handlers = None,
        message_handlers = None,
        disconnect_handlers = None
    ):
    """
    Create a websocket server and launch it.

    app = The Flask app that this websocket server will wrap.
    port = The port to launch the server on.
    connect_handlers = A list of functions to execute, as fn(connectionId),
        whenever a client connects to the websocket.
    message_handlers = A list of functions to execute, as fn(messageData),
        where messageData is a dictionary, whenever we receive a message.
    disconnect_handlers = A list of functions to execute, as fn(connectionId),
        whenever a client disconnects from the websocket.
    """

    # Replace None with an empty list when applicable.
    connect_handlers = [] if connect_handlers is None else connect_handlers
    message_handlers = [] if message_handlers is None else message_handlers
    disconnect_handlers = [] if disconnect_handlers is None else disconnect_handlers

    # Add the handlers as subscribers.
    connect_subscribers.extend(connect_handlers)
    message_subscribers.extend(message_handlers)
    disconnect_subscribers.extend(disconnect_handlers)

    # Create the server and start listening.
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', port)), app)

def send_message(messageData):
    """
    Send the given python dictionary to all clients.
    """
    sio.emit("message", json.dumps(messageData))

@sio.on("connect", namespace="/")
def socket_connect(sid, environ):
    """
    On connection, notify all subscribers
    """
    for sub in connect_subscribers:
        sub(sid)

@sio.on('message', namespace='/')
def message(sid, data):
    """
    On message, notify all subscribers
    """
    for sub in message_subscribers:
        sub(data)

@sio.on('disconnect', namespace='/')
def disconnect(sid):
    """
    On disconnection, notify all subscribers.
    """
    for sub in disconnect_subscribers:
        sub(sid)
