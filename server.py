from flask import Flask
from flask import render_template
from libs.socket_helper import create_socket_server, send_message
from threading import Thread
from sniffer import Sniffer
import signal
import sys


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
signal.pause()


PORT = 8000
app = Flask(__name__)
app.debug = True

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

if __name__ == "__main__":
    def dummy_message_handler(message):
        print("Just got message " + str(message))
        send_message({"message": "Welcome to the app!"})
    
    present_sniffer = Sniffer()
    
    def on_close(signal, frame):
        present_sniffer.stop()

    Thread(target=lambda: present_sniffer.run()).start()
    signal.signal(signal.SIGINT, on_close)
    create_socket_server(app, PORT, message_handlers=[dummy_message_handler])
