# Generously adapted (like a boss!) from
# http://voorloopnul.com/blog/a-python-proxy-in-less-than-100-lines-of-code/
import socket
import select
import time
import sys

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
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
    input_list = []
    channel = {}

    def __init__(self, lhost, lport, fhost, fport):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((lhost, lport))
        self.server.listen(200)
        self.input_list.append(self.server)
        self.fhost = fhost
        self.fport = fport 

    def communicate(self):
        inputready, outputready, exceptready = select.select(self.input_list, [], [])
        for self.s in inputready:
            if self.s == self.server:
                self.on_accept()
                break
            self.data = self.s.recv(buffer_size)
            if len(self.data) == 0:
                self.on_close()
            else:
                self.on_recv()

    def on_accept(self):
        forward = Forward().start(self.fhost, self.fport)
        clientsock, clientaddr = self.server.accept()
        if forward:
            print clientaddr, "has connected"
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            print "Can't establish connection with remote server.",
            print "Closing connection with client side", clientaddr
            clientsock.close()

    def on_close(self):
        print self.s.getpeername(), "has disconnected"
        #remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        print data
        self.channel[self.s].send(data)

