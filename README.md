# EchoChamber
A protocol testing platform that simulates network conditions and peer behavior to
produce programmer-friendly benchmark data.

## Goals

1. Enable automated testing of a protocol implementation
    * under a variety of network conditions
    * with peers exhibiting a variety of different behaviors
2. Super easy test configuration
    * Want to avoid having to write a bunch of Go/C++ to test
3. Provide useful reports about how each peer behaves and what performance was like overall

## Features

1. The ability to spin up an arbitrary number of clients
2. Facilitate communication between peers in a natural way
3. Provide a simple configuration language or API
4. Simulate an internal network as well as management of peers
5. Produce programmer-friendly logs/reports about tests

## Dependencies

EchoChamber is designed to run on Unix-like systems and is developed on Debian (https://debian.org). The Prosody XMPP server (https://prosody.im), the np1sec library, and Python PIP (https://pip.pypa.io/) are required on the testing system.  Prosody and Python PIP  may be installed via the operating system's package manager (apt, yum), while np1sec must be installed from source.  Please refer to the README in the np1sec Github project (https://github.org/equalitie/np1sec) for installation instructions.

## Setup

Command examples preceded with a `$` are meant to be run as a normal user account, while examples preceded with a `#` are meant to be run with superuser or root privileges.
```
$ git clone https://github.org/equalitie/EchoChamber.git
...
$ cd EchoChamber
# pip install -r requirements.txt
```

## Running

The config.yml must be customized before EchoChamber can be run:
- `ld_library_path` contains the filesystem path for the custom libraries required by np1sec; primarily libgcrypt.  This value is usually `/usr/local/lib`
- `np1sec_path` is the filesystem path where np1sec was built, this directory contains the jabberite np1sec test client used by EchoChamber.
- `prosody_cmd` is the path to the prosody daemon controlled by EchoChamber

Edit and save config.yml before continuing.

As well, EchoChamber spawns a prosody daemon on demand - any other prosody instance on the system must be stopped before a test can run.

EchoChamber has several command line options, but all are optional:
- `-c/--config` may be used to specify a custom configuration file (default is `config.yml`)
- `-d/--data` specifies the path to the data file describing the tests to be run by EchoChamber (default is `data.yml`)
- `-t/--timeout` sets the timeout value, in seconds, for every test (default is no timeout)
- `--debug` will print debugging information from np1sec (default is no debugging).

```
$ python echo_chamber -d customtest.yml -t 50 --debug
```
