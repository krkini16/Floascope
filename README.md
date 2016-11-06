# Floascope
Tool for tracking incoming tcp flows into a machine


For development purposes, we assume you're running Linux 3.x+, python 2 (python package eventlet is not yet compatible with python3)

We highly recommend using a [Python virtual environment](https://virtualenv.pypa.io/en/stable/).

```
virtualenv -p /usr/bin/python2.7 py2env
```

To run the app, ensure that you have [`pip`](https://pip.pypa.io/en/stable/) installed and run:

```
pip install -r requirements.txt
```

To ensure scraping is properly done, run

```
apt-get install scapy
apt-get install python-socketio


```



Among other tools, this should automatically install libpcap and other dependencies.
