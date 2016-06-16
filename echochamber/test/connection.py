from base import BaseTest
import time

class ConnectionTest(BaseTest):
    def _setup_clients(self): 
        for client_data in self.test_data["clients"]:
            self.clients.append(Client(client_data, self.config, self.debug))
            self._adduser(client_data)
    
    def _score(self):
        if not False in self._results:
            self.result = [True, "%d clients connected to room" % len(self._results)]
        else:
            self.result = [False, "%d clients of %d failed to connect to room" % self._results.count(False)]

    def run(self):
        if not self.start_time:
            self.start_time = time.time()
        for n in range(len(self.clients)):
            client = self.clients[n]
            if n <= self.start_client:
                client.start()
            else:
                continue
            if client.p.poll() is not None:
                continue
            client.inbuf = ""
            join_s = "new session in room%s@%s" % (client.attr["room"], client.attr["server"])
            if join_s in client.outbuf and not client.finished:
                self._results.append( True)
                client.finished=True
                self.start_client += 1
                print "%d clients  %.2fs" % (self.start_client, time.time() - self.start_time)
            client.communicate()
        if len(self._results) == len(self.clients):
            self._score()
            self.cleanup()
