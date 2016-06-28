from echochamber.client import Client
from connection import ConnectionTest
import os
import random

class LoadTest(ConnectionTest):
    def _setup_clients(self):
        for n in range(int(self.test_data["clients"]["count"])):
            account = "client%03d@localhost" % n
            client_data = {
                "account" : account,
                "password" : "password",
                "room" : self.test_data["clients"]["room"],
                "server" : self.test_data["clients"]["server"]}
            sock_path = os.path.join(self.sock_path, client_data["account"])
            self.clients.append(Client(client_data, self.config, sock_path, self.debug))
            self._adduser(client_data)
