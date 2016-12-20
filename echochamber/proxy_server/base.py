# Generously adapted (like a boss!) from
# http://voorloopnul.com/blog/a-python-proxy-in-less-than-100-lines-of-code/
import socket
import select

buffer_size = 4096


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print e
            return False


class BaseProxyServer(object):
    def __init__(self, lhost, lport, fhost, fport):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((lhost, lport))
        self.server.listen(0)
        self.input_list = [self.server]
        self.channel = {}
        self.fhost = fhost
        self.fport = fport
        self.modulo = None

    def communicate(self):
        inputready, outputready, exceptready = select.select(self.input_list, [], [], 0)
        for self.s in inputready:
            if self.s == self.server:
                self.on_accept()
                break
            self.data = self.s.recv(buffer_size)
            if len(self.data) > 0:
                self.on_recv()

    def on_accept(self):
        forward = Forward().start(self.fhost, self.fport)
        clientsock, clientaddr = self.server.accept()
        if forward:
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            clientsock.close()

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        self.channel[self.s].send(data)
