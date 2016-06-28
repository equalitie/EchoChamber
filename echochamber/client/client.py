import subprocess
import os
import select
import shlex
import fcntl
import socket

def read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ""

class Client:
    def __init__(self, client, config, sock_path, debug=False):
        self.debug = debug
        jabberite = os.path.join(config["np1sec_path"], "jabberite")
        port = ""
        if "port" in client.keys():
            port = " --port=%s " % str(client["port"])
        self.command = jabberite +" --account=" + client["account"]+ " --password=\""+ client["password"] + "\" --server=" +  client["server"] + " --room=" + client["room"] + port
        self.env={"LD_LIBRARY_PATH": os.path.join(config["np1sec_path"], ".libs") + ":" + config["ld_library_path"]}
        self.attr = client
        # our process and debugging socket
        self.p = None
        self.s = None
        self.c = None
        # for our select fds and msg buffers
        self.inputs = []
        self.outputs = []
        self.inbuf = ""
        self.outbuf = ""
        self.errbuf = ""
        # [XXX] should keep this state in the test class, not here
        self.finished = False
        self.sock_path = sock_path

    def  _create_sock(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.isfile(self.sock_path):
            os.unlink(self.sock_path)
        sock.bind(self.sock_path)
        sock.listen(1)
        return sock

    def start(self):
        if not self.s:
            self.s = self._create_sock()
            self.outputs.append(self.s)
        if not self.p:
            self.p = subprocess.Popen(shlex.split(self.command), shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr = subprocess.PIPE, env=self.env)
            self.outputs.extend([self.p.stdout, self.p.stderr])

    def cleanup(self):
        if self.p:
            self.p.kill()
            if self.debug:
                print "starting %s" % self.command

    def communicate(self):
        r,w,e = select.select(self.outputs, self.inputs, [],0)
        for fd in r:
            if fd == self.p.stdout:
                self.outbuf = read(self.p.stdout)
                if self.debug:
                    print self.attr["account"],self.outbuf,
            if fd == self.p.stderr:
                self.errbuf = read(self.p.stderr)
                if self.debug:
                    print self.attr["account"],self.errbuf,
            if fd == self.s:
                self.c, address = self.sock.accept()
                self.outputs.append(self.c)
                self.inputs.append(self.c)
            if fd == self.c:
                size = int(self.c.recv(4))
                self.outbuf = self.c.recv(size)
                print self.outbuf

        for fd in w:
            if fd == self.c:
                if len(self.inbuf) > 0:
                    self.c.sendall("%d%s" % (len(self.inbuf), self.inbuf))
                    self.inbuf = ""
