import subprocess
import yaml
import os
import select
from time import sleep
from getopt import getopt, GetoptError
from sys import argv

from test import ConnectionTest
from client import Client 

def run_test(test, config, debug=False):
    test_clients = []
    for client in test["clients"]:   
        c = Client(client, config, debug)
        if test["test"] == "connection":
            test_client = ConnectionTest(c)
            test_clients.append(test_client)
    fails = 0
    aborts = 0
    while True:
        sleep(.5)
        pop = []
        for n in range(len(test_clients)):
            test = test_clients[n]
            test.run()
            if isinstance(test.result, bool) or test.client.process.poll() != None:
                if not test.result:
                    fails += 1
                else:
                    aborts += 1
                pop.append(n)
        for n in sorted(pop, reverse=True):
            del test_clients[n]
        if len(test_clients) == 0:
            break
    return fails, aborts

def run_tests(tests, config, debug=False):
    for test in tests:
        fails, aborts = run_test(test, config, debug)
        if fails > 0:
            print "test '%s' failed %d times with %d aborts" % (test["name"], fails, aborts)
        else:
            print "test '%s' passed with %d aborts" % (test["name"], aborts)


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
    tests = yaml.load(file(test_file, "r"))
    run_tests(tests, config, debug=True)    
