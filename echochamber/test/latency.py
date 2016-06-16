from connection import ConnectionTest

class LatencyTest(ConnectionTest):
    def _setup_clients(self):
        for n in range(len(self.test_data["clients"])):
            client_data = self.test_data["clients"][n]
            client_data["port"] = 5223 + n
            self.clients.append(Client(client_data, self.config, self.debug))
            self._adduser(client_data)
            self.proxy_server = LatencyProxyServer("localhost", client_data["port"], self.server_host, 5222, int(client_data["latency"]))

    def run(self):
        self.proxy_server.communicate()
        super(self.__class__, self).run()
