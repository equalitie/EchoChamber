EchoChamber
===========

[![CircleCI](https://circleci.com/gh/equalitie/EchoChamber/tree/pytest-expect.svg?style=svg)](https://circleci.com/gh/equalitie/EchoChamber/tree/pytest-expect)

EchoChamber is test harness and set of integration tests for the [np1sec](https://github.com/equalitie/np1sec) library. The platforms simulates real-world network conditions and peer behavior to produce programmer-friendly benchmark data.

## Goals

* Enable automated testing of a protocol implementation
   * under a variety of network conditions
   * with peers exhibiting a variety of different behaviors
* High level test interface
   * Avoid the need to write lots of C++ test code
* Provide useful reports about how each peer behaves and what performance was like overall

## Features

1. The ability to spin up an arbitrary number of clients
2. Facilitate communication between peers in a natural way
3. Provide a simple configuration language or API
4. Simulate an internal network as well as management of peers
5. Produce programmer-friendly logs/reports about tests

## Setup

EchoChamber uses the **py.test** test framework to manage and run tests. All of the integration tests use the test np1sec client **Jabberite** and a local XMPP server. We recommend using a local **Prosody** XMPP server to more emulate a realistic client-server chat network.

First the np1sec library and Jabberite client must be built from source. Please refer to the README in the np1sec Github project (https://github.org/equalitie/np1sec) for installation instructions.

Next clone this git repository to your machine. It should be cloned to the same parent directory as the np1sec library:

      git clone git@github.com:equalitie/EchoChamber.git
      cd EchoChamber

On a Debian-based system the Prosody XMPP server and test dependencies can be installed as follows:

      sudo apt-get install prosody
      sudo service prosody stop # Stop the default prosody server
      pip install -r requirements.txt

# Setup

Clone this git repository to your machine. Rename `config.yml.example` to `config.yml` and edit the file as appropriate.

To run EchoChamber, you need to install dependencies first, by launching:

      pip install -r requirements.txt

# Running

EchoChamber uses the `pytest` framework for collecting and running EchoChamber tests. The EchoChamber specific pytest options are listed in the pytest help message (`py.test --help`).


      --show-cli-output     show output from all subprocesses (v. noisy)
      --debug-mode          Enable debug features such as interactive prompts and
                            invitation of external jabberite clients.
      --run-with-gdb        Run jabberite instances with GDB.
      -C ECHOCHAMBER_CONFIG, --echochamber-config=ECHOCHAMBER_CONFIG
                            Location of the EchoChamber config file.

As EchoChamber is based on `pytest`, all of it's [standard options](http://doc.pytest.org/en/latest/usage.html) are available for use.

### Test Invocation

Running the tests without interactive output:

    py.test

Running the tests with extra logging:

    py.test -s -v

Running the tests in debug mode:

    py.test -s -v --debug-mode

A subset of tests can be run by providing a set of test filenames to run:

    py.test -s -v test_connection.py
