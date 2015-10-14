# Client wrappers

In order for the Chamber test server to interact with your client implementation without
having to extend the EchoChamber software itself to have a specific understanding of your
software's interface, a simple HTTP communication layer is used.  Put simply, your client
should present an HTTP interface that the Chamber server can use to notify your client
when messages arrive and also that will communicate a client's desire to send a message
to the Chamber server.

Fortunately, the interface between the Chamber server and your client implementation
is extremely simple, which could mean it is possible for your client to exist behind a
single HTTP request handler.

## Start a new client

### Chamber

The enpoint for having Chamber start a new client is as follows:

Method | Route   | Parameters
-------|---------|------------
POST   | /client | `{"id": string}`

### Client

Clients will have to be prepared to receive a message about their having joined a session

Method | Route   | Parameters
-------|---------|------------
POST   | /joined | `{"id": string, "participants": [string]}`

## Disconnect a client

### Chamber

The endpoint for having Chamber signal a client to disconnect is:

Method | Route   | Parameters
-------|---------|------------
DELETE | /client | `{"id": string}`

### Client

Clients will have to be prepared to receive a message so they can gracefully quit

Method | Route       | Parameters
-------|-------------|------------
POST   | /disconnect | N/A

## Stimulate message send

### Chamber

To instruct Chamber to prompt a client to send a message other than what it may be
programmed to send, the following endpoint is available:

Method | Route       | Parameters
-------|-------------|------------
POST   | /prompt     | `{"from": string, "to": string, "message": string}`

**NOTE** that Chamber will match the "from" field's value and the "to" field's value
so that multiple clients can be prompted to send or be targeted as receivers if desired.

### Client

In order to receive the prompt, clients should be prepared for messages on the following route:

Method | Route       | Parameters
-------|-------------|------------
POST   | /prompt     | `{"from": string, "to": string, "message": string}`

This is exactly the same as the Chamber endpoint.

In order for a client to send a message to Chamber to be sent to another client, it can use
the following endpoint:

Method | Route       | Parameters
-------|-------------|------------
POST   | /send       | `{"from": string, "to": string, "message": string}`

**NOTE** that Chamber will match the "from" field's value and the "to" field's value
so that multiple clients can be prompted to send or be targeted as receivers if desired.

The reason for a separate route to be used here is to prevent infinite prompting from occurring,
and also to make it easier for clients to send messages unprompted.
