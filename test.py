from client import Client
import os
class ConnectionTest:
    def __init__(self, clients, config, debug):
        self.clients = []
        for client in clients:
            self.clients.append(Client(client, config, debug))
        self._results = None
        self.result = None
    
    def _end(self, client, result):
        self._results.append(result)
        client.kill()

    def _score(self):
        max_ = 0
        for result in self._results:
            if result == False:
                self.result = (False, "Client failed to connect")
                break
            # Ugly, but will do until we have a debug channel for the client
            num = int(result.split("currently ")[1].split(" ")[0]) 
            if num > max_:
                max_ =  num_participants

        if max_ == len(self.clients):
            self.result = (True, "%d clients connected to room" % max_)
        else:
            self.result = (False, "%d clients of %d failed to connect to room" % (len(self.clients) - _max, len(self.clients)))

    def run(self):
        for client in self.clients:
            if client.poll() is not None:
                continue
            client.inbuf = ""
            join_s = "join: %s: currently" % client.attr["account"].split("@")[0]
            if client.errbuf.count(join_s) == 1:
                self._end(client.errbuf)
            if client.errbuf.count("np1sec can not send messages to room"):
                self._end(False)
            client.communicate()
        if len(self._results) == len(self.clients):
            self._score_test()
