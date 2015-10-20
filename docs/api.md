# Client wrappers

In order for the Chamber test server to interact with your client implementation without
having to extend the EchoChamber software itself to have a specific understanding of your
software's interface, a simple HTTP communication layer is used.  Put simply, your client
should present an HTTP interface that the Chamber server can use to notify your client
when messages arrive and also that will communicate a client's desire to send a message
to the Chamber server.

Fortunately, the interface between the Chamber server and your client implementation
is extremely simple.

## Chamber API Endpoints

The following table presents all of the endpoints chamber provides for configuring the
running test, configuring the network settings, and handling clients.

<table>
    <tr>
        <th>Entity</th>
        <th>General</th>
        <th>Actions</th>
    </tr>
    <tr>
        <td><a href="#">Clients</a></td>
        <td>
            <ul>
                <li><a href="#">Create</a></li>
                <li><a href="#">Notify of join</a></li>
                <li><a href="#">Notify of receipt</a></li>
            </ul>
        </td>
        <td>
            <ul>
                <li><a href="#">Disconnect</a></li>
                <li><a href="#">Prompt to send</a></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td><a href="#">Config</a></td>
        <td>
            <ul>
            </ul>
        </td>
        <td>
            <ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td><a href="#">Network</a></td>
        <td>
            <ul>
            </ul>
        </td>
        <td>
            <ul>
            </ul>
        </td>
    </tr>
</table>

## Client API Endpoints

The following table presents all of the endopints a client must provide in order to be
controlled properly by Chamber.

Method | Route       | Parameters                                            | Description
-------|-------------|-------------------------------------------------------|------------
POST   | /joined     | `{"id": string, "participants": [string]}`            | Notify the client that it has joined the test session and been assigned an ID
POST   | /received   | `{"from": string, "message": string, "date": string}` | Notify the client that it has been sent a message
POST   | /prompt     | `{"to": string, "message": string}`                   | Prompt the client to send a message to another client
POST   | /disconnect | N/A                                                   | Notify the client that it has been disconnected from the test session

### Client Joined

Parameter    | Examples         | Description
-------------|------------------|-------------
id           | idab01, client-1 | The identifier assigned to the client by the tester
participants | [idab02, friend] | A list of identifiers of participant clients in the test session

### Client Receipt

Parameter    | Examples                       | Description
-------------|--------------------------------|-------------
from         | idab00, client-2               | The identifier of the client from whom the message was received
message      | "Hey there!"                   | The content of the message sent
date         | "Tue Nov 10 23:00:00 UTC 2009" | A unix-date formatted datestring set when chamber got the message

### Client Prompt

Parameter | Examples            | Description
----------|---------------------|-------------
to        | friend0, id01       | The identifier of the client that the prompted client should send to
message   | "Nice to meet you." | The message that the prompted client should send
