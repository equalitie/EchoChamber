from latency import LatencyProxyServer
import time
import random


# we are using a latency proxy server, and reordering the queued messages
# hardcoding latency with hopes that enough messages will be queued for
# shuffling
class ReorderProxyServer(LatencyProxyServer):
    def on_recv(self):
        if self.s not in self.queue.keys():
            self.queue[self.s] = {}
        future = time.time() + self.latency
        self.queue[self.s][future] = self.data
        if len(self.queue[self.s].keys()) > 0:
            vals = self.queue[self.s].values()
            keys = self.queue[self.s].keys()
            random.shuffle(vals)
            self.queue[self.s] = dict(zip(keys, vals))
