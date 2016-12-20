from base import BaseProxyServer
import time


class LatencyProxyServer(BaseProxyServer):
    def __init__(self, host, port, fhost, fport, latency=0):
        super(LatencyProxyServer, self).__init__(host, port, fhost, fport)
        self.latency = latency / 1000.0
        self.queue = {}

    def communicate(self):
        super(LatencyProxyServer, self).communicate()
        now = time.time()
        pop = {}
        for s, q in self.queue.items():  # a distinct queue for each channel
            pop[s] = []
            for t in q.keys():
                if t <= now:
                    data = q.pop(t)
                    self.channel[s].send(data)

    def on_recv(self):
        if self.s not in self.queue.keys():
            self.queue[self.s] = {}
        future = time.time() + self.latency
        # uncomment to debug
        # print future, self.data
        self.queue[self.s][future] = self.data
