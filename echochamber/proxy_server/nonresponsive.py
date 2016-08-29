from base import BaseProxyServer
import time
import random

class NonResponsiveProxyServer(BaseProxyServer):
    def __init__(self, host, port, fhost, fport):
        super(NonResponsiveProxyServer, self).__init__(host, port, fhost, fport)
        self.msg_count = {} # dictionary to hold message counts
        # once joined, the proxy server stops responding
        self.joined = False

    def on_recv(self):
        if self.s not in self.msg_count.keys():
            self.msg_count[self.s] = 0
        self.msg_count[self.s] += 1
        if self.msg_count[self.s] % self.modulo and not self.joined:
            self.channel[self.s].send(self.data)
