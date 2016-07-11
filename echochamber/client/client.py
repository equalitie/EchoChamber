import subprocess
import os
import select
import shlex
import fcntl
import socket
import struct
import json

def read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ""

class Client(object):
    def __init__(self, client, config, sock_path, debug=False):
        self.debug = debug
        jabberite = os.path.join(config["np1sec_path"], ".libs", "ecjabberite")
        port = ""
        if "port" in client.keys():
            port = " --port=%s " % str(client["port"])
        self.command = jabberite +" --account=" + client["account"]+ " --password=\""+ client["password"] + "\" --server=" +  client["server"] + " --room=" + client["room"] + port + " -e " + sock_path
        self.env={"LD_LIBRARY_PATH": os.path.join(config["np1sec_path"], ".libs") + ":" + config["ld_library_path"]}
        if debug:
            print self.command
        self.attr = client
        # our process and debugging socket
        self.p = None
        self.s = None
        self.c = None
        # for our select fds and msg buffers
        self.inputs = []
        self.outputs = []
        self.inbuf = []
        self.outbuf = None
        self.errbuf = ""
        # [XXX] should keep this state in the test class, not here
        self.sock_path = sock_path
        self.pack = struct.Struct(">i")

    def start(self):
        if not self.s:
            self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            if os.path.isfile(self.sock_path):
                os.unlink(self.sock_path)
            self.s.bind(self.sock_path)
            self.s.listen(1)
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
                out = read(self.p.stdout)
                if self.debug:
                    print self.attr["account"], out
            if fd == self.p.stderr:
                out = read(self.p.stderr)
                if self.debug:
                    print self.attr["account"], out
            if fd == self.s:
                self.c, address = self.s.accept()
                self.outputs.append(self.c)
                self.inputs.append(self.c)
            if fd == self.c:
                try:
                    msg = self.c.recv(self.pack.size)
                    size = self.pack.unpack(msg)
                except struct.error:
                    print self.attr["account"], msg
                self.outbuf = json.loads(self.c.recv(size[0]))
                if self.debug:
                    print self.attr["account"], self.outbuf

        for fd in w:
            if fd == self.c:
                for msg in self.inbuf:
                    inbuf = json.dumps(msg)
                    size = self.pack.pack(len(inbuf))
                    self.c.send(size)
                    self.c.send(inbuf)
                self.inbuf = []
