from base import BaseProxyServer
import time

class LatencyProxyServer(BaseProxyServer):
    def __init__(self, host, port, fhost, fport, latency=0):
        super(self.__class__, self).__init__(host, port, fhost, fport)
        self.latency = latency / 1000.0
        self.queue = {}

    def communicate(self):
        super(self.__class__, self).communicate()
        now = time.time() 
        pop = {}
        for s,q in self.queue.items(): # a distinct queue for each channel
            pop[s] = []
            for n in range(len(q)):
                data = q[n]
                if data[1] <= now:
                    self.channel[s].send(data[0])
                    pop[s].append(n)
        for s,p in pop.items():
            for n in sorted(p, reverse=True):
                del self.queue[s][n]

    def on_recv(self):
        if self.s not in self.queue.keys():
            self.queue[self.s] = []
        future = time.time() + self.latency
        # uncomment to debug
        #print future, self.data
        self.queue[self.s].append((self.data, future))
