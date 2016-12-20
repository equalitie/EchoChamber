from base import BaseProxyServer


class DropProxyServer(BaseProxyServer):
    def __init__(self, host, port, fhost, fport, modulo):
        super(DropProxyServer, self).__init__(host, port, fhost, fport)
        self.msg_count = {}  # dictionary to hold message counts
        # drop every modulo packet
        self.modulo = modulo

    def on_recv(self):
        if self.s not in self.msg_count.keys():
            self.msg_count[self.s] = 0
        self.msg_count[self.s] += 1
        if self.msg_count[self.s] % self.modulo:
            self.channel[self.s].send(self.data)
