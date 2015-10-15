# Client wrappers

In order for the Chamber test server to interact with your client implementation without
having to extend the EchoChamber software itself to have a specific understanding of your
software's interface, a simple HTTP communication layer is used.  Put simply, your client
should present an HTTP interface that the Chamber server can use to notify your client
when messages arrive and also that will communicate a client's desire to send a message
to the Chamber server.

Fortunately, the interface between the Chamber server and your client implementation
is extremely simple.

## Start a new client

### Chamber

The enpoint for having Chamber start a new client is as follows:

Method | Route   | Parameters
-------|---------|------------
POST   | /client | `{"id": string}`

The `id` field here is the unique identifier assigned to the new client.

### Client

Clients will have to be prepared to receive a message about their having joined a session

Method | Route   | Parameters
-------|---------|------------
POST   | /joined | `{"id": string, "participants": [string]}`

The `id` field here is the unique string identifier assigned to the client.
The `participants` field is an array of the identifiers of clients already in the simulation.

## Disconnect a client

### Chamber

The endpoint for having Chamber signal a client to disconnect is:

Method | Route   | Parameters
-------|---------|------------
DELETE | /client | `{"id": string}`

The `id` field is the unique identifier of the client to disconnect.

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

The `from` field is a regular expression that must match one or more client's identifiers.
The `to` field is a regular expression that must match one or more client's identifiers.
The `message` field is the content of the message to send to the recipients.

### Client

In order to receive the prompt, clients should be prepared for messages on the following route:

Method | Route       | Parameters
-------|-------------|------------
POST   | /prompt     | `{"to": string, "message": string}`

The `to` field is a regular expression that matches the the identifiers of recipient clients.
The `message` field is the content of the message to send to the recipients.

## Sending messages

### Chamber

In order for a client to send a message to Chamber to be sent to another client, it can use
the following endpoint:

Method | Route       | Parameters
-------|-------------|------------
POST   | /send       | `{"to": string, "message": string}`

The `to` field is a regular expression that matches the the identifiers of recipient clients.
The `message` field is the content of the message to send to the recipients.

### Client

In order to be notified when a message has arrived for the client, it must provide the following
endpoint:

Method | Route       | Parameters
-------|-------------|------------
POST   | /received   | `{"from": string, "message": string, "date": string}`

The `from` field is the identifier of the client that sent the message.
The `message` field is the content of the message sent.
The `date` field is a Unix-date-formatted timestamp of when the message was sent.
For example, `"Tue Nov 10 23:00:00 UTC 2009"`.
