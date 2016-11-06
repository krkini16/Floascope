from flask import Flask
import eventlet
eventlet.monkey_patch()
from flask import render_template
from sniffer import Sniffer

from flask_socketio import SocketIO, emit


PORT = 8000
app = Flask(__name__)
app.config['SECRET_KEY'] = 'kmh_floascope'
socketio = SocketIO(app, async_mode="eventlet")
app.debug = True
thread = None

@app.route("/")
def sankey():
    """
    The default route will serve sankey.html.
    """
    return render_template("sankey.html")

@app.route("/ts")
def timeseries():
    """
    The default route will serve sankey.html.
    """
    return render_template("timeseries.html")


@app.route("/<path:path>")
def static_proxy(path):
    """
    Serves static files (e.g. CSS, JS) from static/ directory.
    """
    return app.send_static_file(path)

@socketio.on('connect', namespace='/')
def test_connect():
    print("Got a connection")
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=lambda: Sniffer(socketio).run())
    emit('custom_message', {'message': 'Connected'})

@socketio.on('disconnect', namespace='/')
def test_disconnect():
    print('Client disconnected')

@socketio.on('custom_message')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == "__main__":
    socketio.run(app, port=PORT)
