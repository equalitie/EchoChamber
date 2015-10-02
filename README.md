# EchoChamber
A protocol testing platform that simulates network conditions and peer behavior to
produce programmer-friendly benchmark data.

# Goals

1. Enable automated testing of a protocol implementation
    * under a variety of network conditions
    * with peers exhibiting a variety of different behaviors
2. Super easy test configuration
    * Want to avoid having to write a bunch of Go/C++ to test
3. Provide useful reports about how each peer behaves and what performance was like overall

# Features

1. The ability to spin up an arbitrary number of clients 
2. Fascilitate communication between peers in a natural way
3. Provide a simple configuration language or API
4. Simulate an internal network as well as management of peers 
5. Produce programmer-friendly logs/reports about tests
