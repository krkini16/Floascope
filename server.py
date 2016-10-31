from flask import Flask
from flask import render_template
from libs.socket_helper import create_socket_server, send_message

PORT = 8000
app = Flask(__name__)

@app.route("/")
def hello():
    """
    The default route will serve sankey.html.
    """
    return render_template("sankey.html")

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

    create_socket_server(app, PORT, message_handlers=[dummy_message_handler])
