import os
class ConnectionTest:
    def __init__(self, client):
        self.client = client
        self.result = None
    
    # simple connection test
    def run(self):
        if self.client.errbuf.count("Initialized user_state") == 1:
            self.client.inbuf = "Hello" + os.linesep
        if self.client.errbuf.count("Client connected"): # [XXX] placeholder til we get the actual connection string
            self.result = True
        if self.client.errbuf.count("np1sec can not send messages to room"):
            self.result = False
        self.client.communicate()
