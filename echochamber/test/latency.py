from echochamber.proxy_server import LatencyProxyServer
from echochamber.client import Client
from connection import ConnectionTest

class LatencyTest(ConnectionTest):
    def _setup_clients(self):
        self.proxy_servers = []
        for n in range(len(self.test_data["clients"])):
            client_data = self.test_data["clients"][n]
            client_data["port"] = 5224 + n
            self.proxy_servers.append(LatencyProxyServer("localhost", client_data["port"], self.server_host, 5222, int(client_data["latency"])))
            self.clients.append(Client(client_data, self.config, self.debug))
            self._adduser(client_data)

    def run(self):
        for proxy_server in self.proxy_servers:
            proxy_server.communicate()
        super(self.__class__, self).run()
