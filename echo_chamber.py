import subprocess
import yaml
import os
import select
import time
from getopt import getopt, GetoptError
from sys import argv
import shlex

from echochamber.test import *

def run_test(test_data, config, debug, timeout=0):
    if test_data["test"] == "connection":
        Test = ConnectionTest
    elif test_data["test"] == "load":
        Test = LoadTest
    elif test_data["test"] == "latency":
        Test = LatencyTest
    elif test_data["test"] == "messaging":
        Test = MessagingTest
    elif test_data["test"] == "reorder":
        Test = ReorderTest
    test = Test(test_data, config, debug)
    start = time.time()
    try:
        while True:
            time.sleep(0.001)
            test.run()
            elapsed = time.time() - start
            if test.result is not None:
                return test.result + [elapsed] 
            if timeout:
                if elapsed > timeout:
                    test.cleanup()
                    return [False, "Test failed to complete after %d seconds" % timeout, elapsed]
    except KeyboardInterrupt:
        elapsed = time.time() - start
        test.cleanup()
        return [False, "Test interrupted by user", elapsed]

if __name__ == "__main__":
    try:
        optlist, args = getopt(argv[1:], "c:d:t:", ["config", "data", "debug", "timeout"])
    except GetoptError as e:
        print str(e)
    config_file = "config.yml"
    test_file = "data.yml"
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
    data = yaml.load(file(test_file, "r"))
    for test_data in data:
        result = run_test(test_data, config, debug, timeout)    
        if result == None:
            print "FAIL for [%s]: test uncompleted" % test_data["name"]
        if result[0]:
            print "PASS for [%s]: %s\n\tTime Elapsed: %f" % (test_data["name"], result[1], result[2])
        else:
            print "FAIL for [%s]: %s\n\tTime Elapsed: %f" % (test_data["name"], result[1], result[2])
