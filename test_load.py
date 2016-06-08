from client import Client
from test_connection import ConnectionTest
from utils import add_prosody_user
import os
import random

class LoadTest(ConnectionTest):
    def _setup_clients(self, clients, config, debug):
        for n in range(int(clients["count"])):
            account = "client%03d@localhost" % n
            client_data = {
                "account" : account,
                "password" : "password",
                "room" : clients["room"],
                "server" : clients["server"]}
            self.clients.append(Client(client_data, config, debug))
            add_prosody_user(client_data)
