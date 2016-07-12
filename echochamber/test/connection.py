from base import BaseTest
import time

class ConnectionTest(BaseTest):
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
            if "parallel" in self.test_data.keys() and self.test_data["parallel"]:
                client.start()
            elif n <= self.start_client:
                client.start()
            else:
                continue
            if client.p.poll() is not None:
                continue
            account = client.attr["account"].split("@")[0]
            if not client.outbuf:
                pass
            if (client.outbuf and client.outbuf["request"] == "joined" and 
                    account in client.outbuf["participants"] and client not in self.connected):
                self._results.append(True)
                self.connected.append(client)
                self.start_client += 1
                print "%d clients  %.2fs" % (self.start_client, time.time() - self.start_time)
                client.outbuf = None
                client.inbuf = msg
            client.communicate()
        if len(self._results) == len(self.clients):
            self._score()
            self.cleanup()
