from latency import LatencyProxyServer
import time
import random

class DropProxyServer(LatencyProxyServer):
    def __init__(self, host, port, fhost, fport, modulo):
        super(DropProxyServer, self).__init__(host, port, fhost, fport)
        self.msg_count = {} # dictionary to hold message counts
        # drop every modulo packet
        self.modulo = modulo

    def on_recv(self):
        if self.s not in self.queue.keys():
            self.queue[self.s] = {}
            self.msg_count[self.s] = 0
        self.msg_count[self.s] += 1
        if self.msg_count[self.s] % self.modulo:
            future = time.time() + self.latency
            self.queue[self.s][future] = self.data
