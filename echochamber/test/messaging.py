from base import BaseTest
import time

class MessagingTest(BaseTest):
    def __init__(self, test_data, config, debug):
        super(self.__class__, self).__init__(test_data, config, debug)
        self.msg_in = self._setup_msg_in()
        self.msg_in_done = {}
        self.msg_out = {}

    def _setup_msg_in(self):
        # in seconds
        total_time = int(self.test_data["total_time"])
        # num of messages for frequent messengers
        freq_h = int(self.test_data["frequency_high"])
        # num of messages for less frequent messengers
        freq_l = int(self.test_data["frequency_low"])
        # percentage of users who are frequent messengers
        percent_h = int(self.test_data["percentage_high_users"])
        clients_h = random.sample(self.clients, len(self.clients) * (percent_h / 100.0))
        for client in self.clients:
            self.msg_in[client] = {}
            freq = freq_l
            if client in clients_h:
                freq = freq_h
            for n in range(freq):
                msg = {
                    "request":"prompt",
                    "to": "%s@%s" % (client.attr["room"],client.attr["server"]),
                    "message":''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randrange(14,100))}
                self.msg_in[client][random.uniform(2, total_time)] = msg

    def _score(self):
        max_t = 0
        for client, msg_in in self.msg_in_done.items():
            out_times = self.msg_out[client].keys()
            in_times = msg_in.keys()
            for n in range(len(out_times)):
                in_time = in_times[n] + self.start_time
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
            if n <= self.start_client:
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
            else: # this client is already connected so check if there are messages
                if "request" in client.outbuf.keys():
                    if client.outbuf["request"] == "received":
                        self.msg_out[client][time.time()] = client.outbuf
                        client.outbuf = None
                # process our input message queue
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
            for client, msgs in self.msg_in_done.items():
                if len(self.msg_out[client].keys()) != len(msgs):
                    finished = False
            if finished:
                self._score()
                self.cleanup()
