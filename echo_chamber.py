import subprocess
import yaml
import os
import select
from time import sleep
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

def run_test(data, config, debug=False):
    for client in data["clients"]:   
        register_prosody_user(client)
    if data["test"] == "connection":
        test = ConnectionTest(clients, config, debug)
    while True:
        test.run()
        if test.result is not None:
            return test.result

if __name__ == "__main__":
    try:
        optlist, args = getopt(argv[1:], "c:t:", ["config", "test"])
    except GetoptError as e:
        print str(e)
    config_file = "config.yml"
    test_file = "test.yml"
    for o, a in optlist:
        if o in ("-c", "--config"):
            config_file = a
        elif o in ("-t", "--test"):
            test_file = a
    config = yaml.load(file(config_file, "r"))
    data = yaml.load(file(test_file, "r"))
    result = run_test(data, config, debug=True)    
    if result[0]:
        print "Test passed: %s" % result[1]
    else:
        print "Test failed: %s" % result[1]
