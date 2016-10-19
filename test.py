from scapy.all import *

sniff(prn=lambda x: x.summary())
