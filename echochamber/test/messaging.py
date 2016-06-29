from base import BaseTest
import time

class MessagingTest(BaseTest):

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
            account = client.attr["account"].split("@")[0]
            if (client.outbuf and client.outbuf["request"] == "joined" and 
               account in client.outbuf["participants"] and 
               client not in self.connected):
                self.connected.append(client)
                self.start_client += 1
                client.outbuf = None
                msg = {"request":"prompt", "to": "%s@%s" % (client.attr["room"],client.attr["server"]), "message":"HELLO WORLD"}
                client.inbuf = msg
            client.communicate()
        if len(self._results) == len(self.clients):
            self._score()
            self.cleanup()
