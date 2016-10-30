import socketio
import eventlet
import eventlet.wsgi
from flask import Flask
from flask import render_template
import json

PORT = 8000
sio = socketio.Server()
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!" #HTML goes here.

@app.route("/sankey/")
def sankey():
    return render_template("sankey.html")

@sio.on('connect', namespace='/')
def connect(sid, environ):
    print("connect ", sid)
    sio.emit("message", json.dumps({"message": "yo"}), room=sid)

@sio.on('message', namespace='/')
def message(sid, data):
    print("message ", data)
    sio.emit('reply', room=sid)

@sio.on('disconnect', namespace='/')
def disconnect(sid):
    print('disconnect ', sid)

@app.route("/<path:path>")
def static_proxy(path):
    """
    Serves static files (e.g. CSS, JS) from static/ directory.
    """
    return app.wsgi_app.send_static_file(path)

if __name__ == "__main__":
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', PORT)), app)
