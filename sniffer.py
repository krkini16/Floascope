from scapy.all import *
import time
from libs.socket_helper import send_message

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

        src = packet[0][IP].src
        if src in self.sources.keys():
            self.sources[src] = (self.sources[src][0], self.sources[src][1] + 1)
        else:
            self.sources[src] = (self.start_time, 1)
