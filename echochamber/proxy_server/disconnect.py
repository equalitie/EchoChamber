from base import BaseProxyServer


class DisconnectProxyServer(BaseProxyServer):
    def __init__(self, host, port, fhost, fport):
        super(DisconnectProxyServer, self).__init__(host, port, fhost, fport)
        self.msg_count = {}  # dictionary to hold message counts
        # once joined, the proxy server stops responding
        self.joined = False

    def communicate(self):
        if self.joined:  # stop communicating once joining the room
            return
        super(DisconnectProxyServer, self).communicate()

    def on_recv(self):
        if self.s not in self.msg_count.keys():
            self.msg_count[self.s] = 0
        self.msg_count[self.s] += 1
        if (not self.modulo or self.msg_count[self.s] % self.modulo) and not self.joined:
            self.channel[self.s].send(self.data)
