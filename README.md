EchoChamber Tests
=================

[![CircleCI](https://circleci.com/gh/equalitie/EchoChamber/tree/pytest-expect.svg?style=svg)](https://circleci.com/gh/equalitie/EchoChamber/tree/pytest-expect)

EchoChamber is test harness and set of integration tests for the np1sec library.

# Setup

Clone this git repository to your machine. Rename `config.yml.example` to `config.yml` and edit the file as appropriate.

To run EchoChamber, you need to install dependencies first, by launching:

      pip install -r requirements.txt

# Running

EchoChamber uses the `pytest` framework for collecting and running EchoChamber tests. The EchoChamber specific pytest options are listed in the pytest help message.


      --show-cli-output     show output from all subprocesses (v. noisy)
      --debug-mode          Enable debug features such as interactive prompts and
                            invitation of external jabberite clients.
      -C ECHOCHAMBER_CONFIG, --echochamber-config=ECHOCHAMBER_CONFIG
                            Location of the EchoChamber config file.

Running the tests without interactive output:

    py.test

Running the test with extra logging:

    py.test -s -v

Running the tests in debug mode:

    py.test -s -v --debug-mode

A subset of tests can be run by providing a set of test file names to py.test:

    py.test -s -v test_connection.py
