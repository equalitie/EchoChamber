from client import Client
import os
class ConnectionTest:
    def __init__(self, client, config, debug):
        self.client_process = Client(client, config, debug)
        self.result = None
	self.client = client
    
    # simple connection test
    def run(self):
	self.client_process.inbuf = ""
	join_s = "join: %s: joining room %s@%s" % (self.client["account"].split("@")[0], self.client["room"], self.client["server"])
	create_s = "join: %s: creating room %s@%s" % (self.client["account"].split("@")[0], self.client["room"], self.client["server"])
        if self.client_process.errbuf.count(join_s) == 1 or self.client_process.errbuf.count(create_s):
            self.result = True
        if self.client_process.errbuf.count("np1sec can not send messages to room"):
            self.result = False
        self.client_process.communicate()
