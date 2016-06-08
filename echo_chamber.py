import subprocess
import yaml
import os
import select
import time
from getopt import getopt, GetoptError
from sys import argv
import shlex

from test import ConnectionTest
from client import Client 

def register_prosody_user(client):
    devnull = open(os.devnull,"w")
    subprocess.call(shlex.split("sudo prosodyctl deluser %s" % client["account"]), stdout=devnull, stderr=devnull)
    addcmd = "sudo prosodyctl adduser %s" % client["account"]
    process = subprocess.Popen(shlex.split(addcmd), stdin=subprocess.PIPE, stderr=devnull, stdout=devnull)
    output = process.communicate(os.linesep.join([client["password"], client["password"]]))

def run_test(data, config, debug, timeout=0):
    start = time.time()
    for client in data["clients"]:   
        register_prosody_user(client)
    if data["test"] == "connection":
        test = ConnectionTest(data["clients"], config, debug)
    while True:
        test.run()
        if test.result is not None:
            return test.result
        if timeout:
            if (time.time() - start) > timeout:
                return (False, "Test failed to complete after %d seconds" % timeout)

if __name__ == "__main__":
    try:
        optlist, args = getopt(argv[1:], "c:d:t:", ["config", "data", "debug", "timeout"])
    except GetoptError as e:
        print str(e)
    config_file = "config.yml"
    test_file = "test.yml"
    debug = False
    timeout = 0
    for o, a in optlist:
        if o in ("-c", "--config"):
            config_file = a
        elif o in ("-d", "--data"):
            test_file = a
        elif o in ("--debug"):
            debug = True
        elif o in ("-t", "--timeout"):
            timeout = int(a)
    config = yaml.load(file(config_file, "r"))
    data = yaml.load(file(test_file, "r"))[0]
    result = run_test(data, config, debug, timeout)    
    if result[0]:
        print "PASS: %s" % result[1]
    else:
        print "FAIL: %s" % result[1]
