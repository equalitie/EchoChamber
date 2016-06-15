import shutil
import time
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
        self.start = None

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
    
    def _score(self):
        if not False in self._results:
            self.result = [True, "%d clients connected to room" % len(self._results)]
        else:
            self.result = [False, "%d clients of %d failed to connect to room" % self._results.count(False)]

    def run(self):
        if not self.start:
            self.start = time.time()
        for n in range(len(self.clients)):
            client = self.clients[n]
            t = time.time() - self.start
            if t > ((n+1) * .5):
                client.start()
            else:
                continue
            if client.p.poll() is not None:
                continue
            client.inbuf = ""
            join_s = "new session in room%s@%s" % (client.attr["room"], client.attr["server"])
            if join_s in client.outbuf or join_s in client.errbuf and not client.finished:
                self._results.append( True)
                client.finished=True
                print client.attr["account"],
            elif client.errbuf.count("np1sec can not send messages to room") and not client.finished:
                client.finished=True
                self._results.append( False)
            client.communicate()
        if len(self._results) == len(self.clients):
            self._score()
            self.cleanup()
