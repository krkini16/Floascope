from scapy.all import *
import time
from libs.socket_helper import send_message

def send_message(msg):
    print msg

class Sniffer:
    def __init__(self, interval=1000):
        self.sources = {}
        self.interval = interval
        self.start_time = None

    def run(self):
        print self.start_time
        sniff(prn=self._process_packet)

    def _process_packet(self, packet):
        current_time = time.time() * 1000
        if self.start_time is None:
            self.start_time = current_time

        #Note: this is being sent purely based off of interval. No persistant memory.
        if current_time - self.start_time > self.interval:
            self.start_time = current_time
            send_message(self.sources)
            self.sources = {}

        source_ip = packet[0][IP].src
        dest_pid = "TBD"
        if "src" in self.sources.keys():
            self.sources[source_ip][num_packets] += 1
        else:
            self.sources[source_ip] = {"time_stamp" : self.start_time,
                                        "dest_pid"  : dest_pid,
                                        "num_packets": 1,
                                        "interval" : self.interval}
s = Sniffer()
s.run()
