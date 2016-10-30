# Floascope
Tool for tracking incoming tcp flows into a machine


For development purposes, we assume you're running Linux 3.x+

We highly recommend using a [Python virtual environment](https://virtualenv.pypa.io/en/stable/).

To run the app, ensure that you have [`pip`](https://pip.pypa.io/en/stable/) installed and run:

```
pip install -r requirements.txt
```

To ensure scraping is properly done, run

```
apt-get install scapy
```

Among other tools, this should automatically install libpcap and other dependencies.
