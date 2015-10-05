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

## Client to Chamber

In order for a client to send a message to the Chamber server for relaying, the following
method is available:

Description                                          | Message
-----------------------------------------------------|-----------
Notify Chamber of a message to be sent by the client | POST /send {message: string}
Response from Chamber upon receipt of message        | {success: boolean, queueIndex: number}

## Chamber to Client

When Chamber receives a message from a client that is to be relayed to another client,
the following request will be made to the client's API:

Description                                          | Message
-----------------------------------------------------|-----------
Notify the client a message has been received for it | POST /received {message: string, from: number, date: string}
Respond to Chamber to acknowledge receipt            | {success: true}
