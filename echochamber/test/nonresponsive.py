from base import BaseTest
from echochamber.proxy_server import NonResponsiveProxyServer
from echochamber.client import Client
from messaging import MessagingTest
import os

class NonResponsiveTest(MessagingTest):
    def __init__(self, test_data, config, debug):
        super(NonResponsiveTest, self).__init__(test_data, config, debug)
        self.joined = False

    def _setup_clients(self):
        self.proxy_servers = []
        num_clients = int(self.test_data["clients"]["count"])
        for n in range(num_clients):
            account = "client%03d@localhost" % n
            client_data = {
                "account": account,
                "password" : "password",
                "room" : self.test_data["clients"]["room"],
                "server" : self.test_data["clients"]["server"],
                "port" : 15224 + n }
            if n  == (num_clients - 2): # second to last client
                client_data["port"] = 15524 + n
                self.proxy_servers.append(NonResponsiveProxyServer("localhost",
                    client_data["port"], self.server_host, 5222)) 
            sock_path = os.path.join(self.sock_path, client_data["account"])
            self.clients.append(Client(client_data, self.config, sock_path,
                self.debug))
            self._adduser(client_data)

    def run(self):
        # only trigger the non-responsive proxy once the client joins 
        if not self.joined:
            for client in self.clients:
                if client.joined == True:
                    client.proxy_server.joined = True
                    self.client_joined = True
        for proxy_server in self.proxy_servers:
            proxy_server.communicate()
        super(NonResponsiveTest, self).run()

    def _score(self):
        pass # still stubbed
