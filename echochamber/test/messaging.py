from load import LoadTest
import time
import random
import string
import os
from echochamber.client import Client

class MessagingTest(LoadTest):
    def __init__(self, test_data, config, debug):
        super(MessagingTest, self).__init__(test_data, config, debug)
        self.msg_in = self._setup_msg_in()
        self.msg_in_done = {}
        self.msg_out = {}

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

    def _setup_msg_in(self):
        msg_in = {}
        # in seconds
        total_time = int(self.test_data["total_time"])
        # num of messages for frequent messengers
        try:
            freq_h = int(self.test_data["frequency_high"])
        except KeyError: 
            freq_h = int(total_time * .8)
        # num of messages for less frequent messengers
        try:
            freq_l = int(self.test_data["frequency_low"])
        except KeyError:
            freq_l = int(total_time * .2)
        # percentage of users who are frequent messengers
        try:
            percent_h = int(self.test_data["percentage_high_users"])
        except KeyError:
            percent_h = 20
        clients_h = random.sample(self.clients, int(len(self.clients) * (percent_h / 100.0)))
        for client in self.clients:
            msg_in[client] = {}
            freq = freq_l
            if client in clients_h:
                freq = freq_h
            for n in range(freq):
                msg = {
                    "request":"prompt",
                    "to": "%s@%s" % (client.attr["room"],client.attr["server"]),
                    "message": "%03d: %s" % (n, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randrange(14,200)))) # prepending serial number for the message to track message sequence
                }
                # [XXX] start messaging 2 seconds after global start time - might 
                # need tweaking for slow joins with large numbers of clients
                msg_in[client][random.uniform(2, total_time)] = msg
        return msg_in

    def _score(self):
        max_t = 0
        for client_out, msgs_out in self.msg_out.items():
            out_times = msgs_out.keys()
            from_ = client_out["account"].split("@")[0]
            for client_in, msgs_in in self.msg_in.items():
                if from_ in msgs_in.keys():
                    for n in range(len(out_times)):
                        in_time = msgs_in[from_][n] + self.start_time
                        out_time = out_times[n]
                        t = out_time - in_time
                        if t > max_t:
                            max_t = t
        threshhold = float(self.test_data["threshhold"])
        if max_t > threshhold:
            self.result = [False, "%02.3f maximum message time exceeds threshhold of %02.3f seconds with %d clients" % (max_t, threshhold, len(self.clients))]
        else:
            self.result = [True, "%d clients sent messages with a %02.3f seconds maximum message time, below %02.3f seconds threshhold time" % (len(self.clients), max_t, threshhold)]

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
            if client not in self.connected:
                if (client.outbuf and client.outbuf["request"] == "joined" and
                        account in client.outbuf["participants"]):
                    self.connected.append(client)
                    self.start_client += 1
                    # set up our per-client msg queues
                    self.msg_in_done[client] = {}
                    self.msg_out[client] = {}
                    client.joined = True
            else: # this client is already connected so check if there are messages
                if "request" in client.outbuf.keys():
                    if client.outbuf["request"] == "received":
                        from_ = client.outbuf["from"]
                        if not from_ in self.msg_out[client].keys():
                            self.msg_out[client][from_] = {}
                        self.msg_out[client][from_][time.time()] = client.outbuf
                        client.outbuf = {}
                # process our input message queue
                if client in self.msg_in.keys():
                    for t in self.msg_in[client].keys():
                        if t + self.start_time <= time.time():
                            msg = self.msg_in[client].pop(t)
                            self.msg_in_done[client][t] = msg
                            client.inbuf.append(msg)
                    if len(self.msg_in[client]) == 0:
                        self.msg_in.pop(client)
            client.communicate()
        if len(self.msg_in) == 0:
            finished = True
            for client_out, msgs in self.msg_out.items():
                from_ = client_out["account"].split("@")[0]
                for client_in, in_msgs in self.msg_in_done.keys():
                    if len(in_msgs[from_]) != len(msgs):
                        finished = False
                        break
                else:
                    continue
                break
            if finished:
                self._score()
                self.cleanup()
