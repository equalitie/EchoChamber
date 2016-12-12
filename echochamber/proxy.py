import socket
import SocketServer
import threading
import logging
import time

buffer_size = 4096

logging.basicConfig(level=logging.DEBUG)


class ProxyInterface(object):
    """
    Class to abstract the proxy communications
    """
    def process_data(self, source, dest):
        """Infinite loop and proxy data between source and destination socket"""
        try:
            while True:
                data = source.recv(buffer_size)
                if len(data) > 0:
                    logging.debug("Received: %d", len(data))
                    dest.write(data)
                else:
                    raise Exception("Connection disconnected")

                # Send any data which has been queued
                # self.send_queued()
        except Exception, e:
            logging.debug(e)
        dest.stop_forwarding()

    def write(self, data):
        """Request refers to external side of the connection"""
        logging.debug("Sending data: %d", len(data))
        self.request.send(data)

    def stop_forwarding(self):
        logging.debug("Stop forwarding for %s", self)
        self.request.close()


class Forwarder(threading.Thread, ProxyInterface):
    """
    Forwarder which connects to the proxy destination
    """
    def __init__(self, source, destination):
        threading.Thread.__init__(self)
        self.source = source
        self.server = source.server

        self.host, self.port = destination
        self.request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request.connect((self.host, self.port))

    def run(self):
        logging.debug("Starting forwarder %s to %s:%d", self, self.host, self.port)
        self.process_data(source=self.request, dest=self.source)


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler, ProxyInterface):
    """
    Threaded TCP request handler which is spawned for each new client connection.
    """
    def handle(self):
        """Handle new connection from a client and forward to the destination"""
        try:
            # Start destination request and proxy running in a new thread
            dest_host, dest_port = self.server.destination
            self.forwarder = Forwarder(self, self.server.destination)
            self.forwarder.start()
        except socket.error:
            logging.warning("Could not connect to proxy destination %s:%d",
                            dest_host, dest_port)
            return

        logging.info("New connection forwarding to %s:%d", dest_host, dest_port)
        self.process_data(source=self.request, dest=self.forwarder)


class ProxyServer(object):
    """
    Class to enscapsulate the threading proxy server

    Each client connection gets spawned out to a new thread.
    """
    def __init__(self, server_tuple, destination):
        self.server = ThreadedTCPServer(server_tuple, ThreadedTCPRequestHandler)
        self.server.destination = destination

        # Start the listening server in another thread
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        server_ip, server_port = self.server.server_address
        logging.info("Proxy server listening on %s:%s", server_ip, server_port)

    def set_latency(self, latency=None):
        """
        Set the latency for each client connection
        """
        self.server.latency = latency

    def stop(self):
        self.server.shutdown()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    # Start
    proxy = ProxyServer(("127.0.0.1", 9000), ("127.0.0.1", 5222))
    try:
        while True:
            time.sleep(1)
    except:
        pass
    print "...server stopping."
    proxy.stop()
