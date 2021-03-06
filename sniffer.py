from scapy.all import *
import time

class Sniffer:
    def __init__(self, socketio, interval=1000, pcap_file=None):
        self.pcap_file = pcap_file
        self.socketio = socketio
        self.sources = {}
        self.interval = interval
        self.start_time = None
        self.enabled = True

    def stop(self):
        self.enabled = False

    def run(self):
        print self.start_time
        print("running sniffer")

        #Reset enabled flag
        self.enabled = True
        if self.pcap_file is None:
            sniff(prn=self._process_packet, filter='tcp')
        else:
            sniff(prn=self._process_packet, filter='tcp', offline=self.pcap_file)

    def _process_packet(self, packet):
        current_time = time.time() * 1000
        if self.start_time is None:
            self.start_time = current_time

        #Note: this is being sent purely based off of interval. No persistant memory.
        if current_time - self.start_time > self.interval:
            self.start_time = current_time
            self.socketio.emit("custom_message", self.sources)
            self.sources = {}

        if IP not in packet[0]:
            return
        source_ip = packet[0][IP].src
        dest_pid = "TBD"
        if source_ip in self.sources.keys():
            self.sources[source_ip]["num_packets"] += 1
        else:
            dport = -1
            try:
                dport = packet[0][IP].dport
            except:
                pass
            self.sources[source_ip] = {"time_stamp" : self.start_time,
                                        "dest_pid"  : dest_pid,
                                        "dest_port" : dport,
                                        "num_packets": 1,
                                        "interval" : self.interval}
