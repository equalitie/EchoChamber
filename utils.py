import subprocess, os, shlex

devnull = open(os.devnull,"w")

def remove_prosody_user(client_data):
    subprocess.call(shlex.split("sudo prosodyctl deluser %s" % client_data["account"]), stdout=devnull, stderr=devnull)

def add_prosody_user(client_data):
    addcmd = "sudo prosodyctl adduser %s" % client_data["account"]
    remove_prosody_user(client_data)
    process = subprocess.Popen(shlex.split(addcmd), stdin=subprocess.PIPE, stderr=devnull, stdout=devnull)
    kutput = process.communicate(os.linesep.join([client_data["password"], client_data["password"]]))
