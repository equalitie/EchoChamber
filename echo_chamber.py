import subprocess
import yaml
import os
import select
from time import sleep
from getopt import getopt, GetoptError
from sys import argv

def run_test(test, config):
    jabberite = config["jabberite_path"] 
    clients = []
    for client in test["clients"]:   
        process = subprocess.Popen([jabberite, "-a %s" % client["account"], "-s %s" % client["server"], "-r %s" % client["room"], "-p %s" % client["password"]], shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr= subprocess.PIPE)
        clients.append(process)
    while True:
        sleep(.5)
        pop = []
        for n in range(len(clients)):

            client = clients[n]
            stdout = client.stdout.fileno()
            stdin = client.stdin.fileno()
            stderr = client.stderr.fileno()
            rlist = [stdout, stderr]
            wlist = [stdin]
            ready = select.select(rlist,wlist,[])
            for fd in ready[0]:
                if fd == stdout:
                    print client.stdout.readline()
                if fd == stderr:
                    print client.stderr.readline()
            for fd in ready[1]:
                if fd == stdin: # redundant since we only have one write fd
                    client.stdin.write("hello")
            if client.poll() != None:
                pop.append(n)
        for n in sorted(pop, reverse=True):
            del clients[n]
        if len(clients) == 0:
            return

def run_tests(tests, config):
    for test in tests:
        run_test(test, config)

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
    run_tests(tests, config)    
