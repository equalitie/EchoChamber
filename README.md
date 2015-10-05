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
2. Fascilitate communication between peers in a natural way
3. Provide a simple configuration language or API
4. Simulate an internal network as well as management of peers 
5. Produce programmer-friendly logs/reports about tests

## Before you get started

If you struggle to understand any of the terminology or notation used in this document, please
refer to the the [general documentation](https://github.com/equalitie/EchoChamber/blob/master/docs/general.md).

## Dependencies

## Setup

## Running

## Usage

### Creating a testable client

Once you've got an implementation of your client ready for testing, you'll have to do two
things:

1. Write a client that will process and generate messages that can be sent to and understood by other clients
2. Write a simple HTTP interface that your client can use to interface with the Chamber server

You can read more about how the HTTP interface for your client should work in
[the client wrapper specification](https://github.com/equalitie/EchoChamber/blob/master/docs/clients.md).
