import subprocess
import os
import select
import shlex

class Client:
    def __init__(self, client, config, debug=False):
        jabberite = os.path.join(config["np1sec_path"], "jabberite")
        command = jabberite +" --account=" + client["account"]+ " --password=\""+ client["password"] + "\" --server=" +  client["server"] + " --room=" + client["room"]
        env={"LD_LIBRARY_PATH": os.path.join(config["np1sec_path"], ".libs") + ":" + config["ld_library_path"]}
        self.p = subprocess.Popen(shlex.split(command), shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr= subprocess.PI, env= env)
        self.inbuf = ""
        self.outbuf = ""
        self.errbuf = ""
        self.attr = client
        self.debug = debug

    def communicate(self):
        self.outbuf = ""
        self.errbuf = ""
        ready = select.select([self.p.stdout, self.p.stderr], [self.p.stdin], [])  
        for fd in ready[0]:
            if fd == self.p.stdout:
                self.outbuf = self.p.stdout.readline()
                if self.debug:
                    print self.outbuf,
            if fd == self.p.stderr:
                self.errbuf = self.p.stderr.readline()
                if self.debug:
                    print self.errbuf,
        for fd in ready[1]:
            if fd == self.p.stdin:
                if self.inbuf:
                    self.p.stdin.write(self.inbuf)

