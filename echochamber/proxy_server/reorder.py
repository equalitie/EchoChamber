from base import LatencyProxyServer
import time
import random

# we are using a latency proxy server, and reordering the queued messages
# hardcoding latency with hopes that enough messages will be queued for
# shuffling
class ReorderProxyServer(LatencyProxyServer):
    def __init__(self, host, port, fhost, fport):
        super(self.__class__, self).__init__(host, port, fhost, fport, latency=.75)
        self.reorder = reorder
        self.queue = {}

    def on_recv(self):
        if self.s not in self.queue.keys():
            self.queue[self.s] = []
        future = time.time() + self.latency
        self.queue[self.s].append((self.data, future))
        if len(self.queue[self.s].keys()) > 0:
            vals = self.queue[self.s].values()
            keys = self.queue[self.s].keys()
            random.shuffle(vals)
            self.queue[self.s] = dict(zip(keys, vals))
