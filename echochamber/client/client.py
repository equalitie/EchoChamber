import subprocess
import os
import select
import shlex
import fcntl

def read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ""

class Client:
    def __init__(self, client, config, debug=False):
        self.debug = debug
        jabberite = os.path.join(config["np1sec_path"], "jabberite")
        server = client["server"]
        if "port" in client.keys():
            server += ":%s" % str(client["port"])
        self.command = jabberite +" --account=" + client["account"]+ " --password=\""+ client["password"] + "\" --server=" +  server + " --room=" + client["room"]
        self.env={"LD_LIBRARY_PATH": os.path.join(config["np1sec_path"], ".libs") + ":" + config["ld_library_path"]}
        self.inbuf = ""
        self.outbuf = ""
        self.errbuf = ""
        self.attr = client
        self.p = None
        if self.debug:
            print self.command, self.env
        self.finished = False

    def start(self):
        if not self.p:
            self.p = subprocess.Popen(shlex.split(self.command), shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr = subprocess.PIPE, env=self.env)

    def cleanup(self):
        if self.p:
            self.p.kill()
            if self.debug:
                print "starting %s" % self.command

    def communicate(self):
        self.outbuf = ""
        self.errbuf = ""
        ready = select.select([self.p.stdout, self.p.stderr], [self.p.stdin], [],0)
        for fd in ready[0]:
            if fd == self.p.stdout:
                self.outbuf = read(self.p.stdout)
                if self.debug:
                    print self.attr["account"],self.outbuf,
            if fd == self.p.stderr:
                self.errbuf = read(self.p.stderr)
                if self.debug:
                    print self.attr["account"],self.errbuf,
        for fd in ready[1]:
            if fd == self.p.stdin:
                if self.inbuf:
                    self.p.stdin.write(self.inbuf)
