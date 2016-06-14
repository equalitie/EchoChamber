import shutil
import shlex
import tempfile
import os
import subprocess
from jinja2 import Template

from client import Client
import signal, psutil

def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for process in children:
        process.send_signal(sig)

class ConnectionTest: # need to abstract this into a proper parent class
    def __init__(self, test_data, config, debug):
        self.test_data = test_data
        self.config = config
        self.debug = debug
        self.tempdir = tempfile.mkdtemp(prefix="echochamber_")
        self.clients = []
        self.null = open(os.devnull,"w")
        self._setup_server()
        self._setup_clients()
        self._results = []
        self.result = None

    def cleanup(self):
        for client in self.clients:
            client.cleanup()
            self._deluser(client.attr)
        shutil.rmtree(self.tempdir)
        kill_child_processes(self.pid)

    def _deluser(self, client_data):
        cmd = shlex.split("prosodyctl --config %s deluser %s" % (self.prosody_config, client_data["account"]))
        subprocess.call(cmd, stdout=self.null, stderr=self.null)


    def _adduser(self, client_data):
        addcmd = "prosodyctl --config %s adduser %s" % (self.prosody_config, client_data["account"])
        self._deluser(client_data)
        process = subprocess.Popen(shlex.split(addcmd), stdin=subprocess.PIPE, stderr=self.null, stdout=self.null)
        process.communicate(os.linesep.join([client_data["password"], client_data["password"]]))

    def _setup_server(self):
        data_path = os.path.join(self.tempdir, "var", "lib", "prosody")
        run_path = os.path.join(self.tempdir, "var", "run", "prosody")
        config_path = os.path.join(self.tempdir, "etc", "prosody")
        certs_path = os.path.join(config_path, "certs")
        log_path = os.path.join(self.tempdir, "var", "log")
        for dir_ in [data_path, run_path, config_path, certs_path, log_path]:
            os.makedirs(dir_)
        t = Template(open("templates/prosody.cfg.lua").read())
        host = "localhost"
        if "server" in self.test_data and "host" in self.test_data["server"]:
            host = self.test_data["server"]["host"]
        t_data = {
            "data_path" : data_path,
            "run_path" : run_path,
            "config_path" : config_path,
            "certs_path" : certs_path,
            "log_path" : log_path,
            "host" : host}
        self.prosody_config = os.path.join(config_path, "prosody.cfg.lua")
        with open(os.path.join(self.prosody_config), "w") as fh:
            fh.write(t.render(t_data))
        cmd = "%s --config %s" % (self.config["prosody_cmd"], self.prosody_config)
        if self.debug:
            print cmd
        self.pid = subprocess.Popen(shlex.split(cmd), stdout=self.null, stderr=self.null).pid

    def _setup_clients(self): 
        for client_data in self.test_data["clients"]:
            self.clients.append(Client(client_data, self.config, self.debug))
            self._adduser(client_data)
    
    def _end(self, client, result):
        self._results.append(result)
        client.cleanup()

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
            self.result = [True, "%d clients connected to room" % max_]
        else:
            self.result = [False, "%d clients of %d failed to connect to room" % (len(self.clients) - _max, len(self.clients))]
        self.cleanup()

    def run(self):
        for client in self.clients:
            if client.p.poll() is not None:
                continue
            client.inbuf = ""
            join_s = "join: %s: currently" % client.attr["account"].split("@")[0]
            if client.errbuf.count(join_s) == 1:
                self._end(client, client.errbuf)
            elif client.errbuf.count("np1sec can not send messages to room"):
                self._end(client, False)
            client.communicate()
        if len(self._results) == len(self.clients):
            self._score_test()
