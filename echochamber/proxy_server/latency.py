from base import BaseProxyServer
import time

class LatencyProxyServer(BaseProxyServer):
    def __init__(self, host, port, fhost, fport, latency=0):
        super(self.__class__, self).__init__(host, port, fhost, fport)
        self.latency = latency / 1000.0
        self.queue = []

    def communicate(self):
        super(self.__class__, self).communicate()
        now = time.time() 
        pop = []
        for n in range(len(self.queue)):
            data = self.queue[n]
            if data[1] >= now:
                self.channel[self.s].send(data[0])
                pop.append(n)
        for n in sorted(pop, reverse=True):
            del self.queue[n]

    def on_recv(self):
        future = time.time() + self.latency
        self.queue.append((self.data, future))
