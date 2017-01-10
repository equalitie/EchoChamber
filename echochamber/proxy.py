import socket
import SocketServer
import threading
import logging
import time
import bisect
import select
import random

buffer_size = 4096

logging.basicConfig(level=logging.INFO)


class ProxyInterface(object):
    """
    Class to abstract the proxy communications
    """

    def get_next_timeout(self):
        """Calculate latency for the next message"""
        mean = self.server.latency_mean         # pylint: disable=no-member
        variance = self.server.latency_variance # pylint: disable=no-member
        assert mean
        assert variance
        return max(0, random.normalvariate(mean, variance))

    def process_data(self, source, dest):
        """Infinite loop and proxy data between source and destination socket"""
        queue = []

        start = time.time()
        next_send_time = None
        timeout = None # None means to wait indefinitely

        while True:
            data = None

            try:
                input_ready, _, _ = select.select([source], [], [], timeout)
                for s in input_ready:
                    assert data == None
                    data = s.recv(buffer_size)
                    if not data:
                        raise Exception("Connection closed")

            except Exception:
                # Close connections when an exception occurs
                logging.info("Connection closed")
                source.close()
                break

            if queue:
                d = queue.pop(0)
                logging.debug("Sending from queue %d", len(d))
                dest.write(d)

            if data:
                logging.debug("Received: %d", len(data))
                queue.append(data);

            timeout = self.get_next_timeout() if queue else None

        # except Exception, e:
        #     logging.debug(e)
        dest.stop_forwarding()

    def write(self, data):
        """Request refers to external side of the connection"""
        logging.debug("Sending data: %d", len(data))
        self.request.send(data)  # pylint: disable=no-member

    def stop_forwarding(self):
        logging.debug("Stop forwarding %s", self)
        self.request.close()  # pylint: disable=no-member


class Forwarder(threading.Thread, ProxyInterface):
    """
    Forwarder which connects to the proxy destination
    """
    def __init__(self, source, destination):
        threading.Thread.__init__(self)
        self.source = source
        self.server = source.server
        self.daemon = True

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
    def __init__(self, server_tuple, destination, latency_mean, latency_variance):
        self.server = ThreadedTCPServer(server_tuple, ThreadedTCPRequestHandler)
        self.server.destination = destination
        self.server.latency_mean = latency_mean
        self.server.latency_variance = latency_variance

        # Start the listening server in another thread
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        server_ip, server_port = self.server.server_address
        logging.info("Proxy server listening on %s:%s", server_ip, server_port)

    def stop(self):
        logging.info("Stopping proxy")
        self.server.shutdown()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    # Start a test instance of the proxy when called directly
    proxy = ProxyServer(("127.0.0.1", 0), ("127.0.0.1", 5222), 2000)
    try:
        while True:
            time.sleep(1)
    except:
        pass
    logging.info("...server stopping.")
    proxy.stop()
