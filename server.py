from flask import Flask
from flask import render_template
from libs.socket_helper import create_socket_server, send_message
from sniffer import Sniffer
import thread

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
    
    def sniffer_connect_handler(message):
        print("CONNECTING" + str(message))
        send_message({"message": "New client connected to server. New Sniffer"})

    def sniffer_message_handler(message):
        print("Just got message " + str(message))        
        send_message({"message": "Server heard from this client. Welcome to the app!"})


    def start_sniffer():
        s = Sniffer()
        s.run()

    def start_server():
        create_socket_server(app, PORT, connect_handlers=[sniffer_connect_handler], message_handlers=[sniffer_message_handler])

    thread.start_new_thread(start_server, ())
    start_sniffer()