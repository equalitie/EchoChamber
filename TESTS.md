# Customizing EchoChamber Tests
EchoChamber tests are defined with a YAML document, and there may be multiple tests in a single document.  The basic format of a test contains three common fields: `name`, `test`, and `clients`. There is an optional parameter `parallel` which forces EchoChamber to start all clients at the same time, by default EchoChamber sequentially connects clients.  Additional fields configure parameters for the specific `test`.

- `test`: Specifies the test to be run
- `name`: This is a description for the test being performed
- `clients`: Depending on the test, this may either be a list of dictionaries describing individual clients, or a single dictionary describing the clients to be spawned for the client- the three parameters are:
-- `count`: the number of clients to spawn
-- `server`: the address of the server for the clients to connect to
-- `room`: the room/channel to establish the np1sec session on

## EchoChamber Test Types
### ConnectionTest - `connection`
`ConnectionTest` is defined in `echochamber/test/connection.py`.  This test spawns a number of clients, connecting them to a room on the server while measuring the amount of time it takes for the final client to join. 

Example ConnectionTest:
```
- name: Load test 100 clients
  test: connection
  clients:
    count: 100
    server: conference.localhost
    room: loadtest
```

### LatencyTest - `latency`
`LatencyTest` measures the performance of the clients when artificial latency is introduced between the connection to the server.  This test also measures the amount of time it takes for the final client to join.

The format for the `clients` field in this test is different from other tests.  Here, individual clients are given names and a value (in milliseconds) for their latency.  This latency value is for each direction from the server to the client.

Example LatencyTest:
```
- name: Latency Test with 5 Clients
  test: latency
  server_host: conference.localhost
  clients:
    - account: bob@localhost
      latency: 40
    - account: jill@localhost
      latency: 400
    - account: phil@localhost
      latency: 200
    - account: alice@localhost
      latency: 1200
    - account: janet@localhost
      latency: 700
```

### MessagingTest - `messaging`
`MessagingTest` measures the performance of clients sending and recieving messages.  There are 5 parameters to customize the test:
- `total_time`: The length of time when clients will be sending messages.
- `percentage_high_users`: The percentage of clients that send a high frequency of messages.
- `frequency_high`: The number of messages which will be sent by the clients (`percentage_high_users`) that send a lot of messages 
- `frequency_low`: The number of messages sent by clients not in the "high frequency" group.
- `threshhold`: The amount of time EchoChamber will wait for the final messages to be received before failing the test.

Messages are strings between 14 and 200 characters in length.

Example MessagingTest:
```
- name: Messaging Test 30 Clients
  test: messaging
  total_time: 200
  frequency_high: 80
  frequency_low: 10
  percentage_high_users: 10
  threshhold: 300
  clients:
    count: 30
    server: conference.localhost
    room: testchat
```

### ReorderTest - `reorder`
Similar to MessagingTest, except that packets from the client are randomly shufled - WorkInProgress.
