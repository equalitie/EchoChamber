package main

import (
    "encoding/json"
    "net/http"
    "os/exec"
    "bytes"
)

/**
 * Represents a client that interfaces with the protocol being tested.
 */
type Client struct {
    PortNumber string
    Identifier string
    executable string
    command    *os.Cmd
}

/**
 * Create a new Client, wrapping an executing client process.
 * The port number that the HTTP server will be running on must be provided here.
 * @param command - The command to run to start the client server. E.g. "./echoclient"
 * @param id - An unique string identifying the client, for internal use
 * @param port - The port number that the client HTTP server will be running on
 */
func NewClient(command, id, port string) Client {
    return Client{port, id, command}
}

/**
 * Start the client server by executing the command provided in the NewClient function
 * with the arguments provided.  Note that, if to specify the port the server runs on,
 * you would provide the port as an argument to the command, the same port number supplied
 * to NewClient should be used here.
 * @param args - Arguments to execute the client command with
 * @return any error occurring while starting the client; see https://golang.org/pkg/os/exec/#Start
 */
func (c *Client)Start(args ...string) error {
    c.command = exec.Command(c.executable, args...)
    return c.command.Start()
}

/**
 * Send POST /joined to the client to let them know they have joined the test simulation
 * and to send a list of the names of clients already in the simulation.
 * @param participants - An array of the identifiers of clients in the simulation
 * @return the response from the client and any error that occurs
 */
func (c *Client)NotifyJoined(participants []string) (*http.Response, error) {
    data, err1 := json.Marshal(JoinedMessage{c.Identifier, participants})
    if err1 != nil {
        return nil, err1
    }
    reader := bytes.NewReader(data)
    request, err2 := http.NewRequest("POST", joinedUrl(c.PortNumber), reader)
    if err2 != nil {
        return nil, err2
    }
    request.Header.Set("Content-Type", "application/json")
    client := &http.Client{}
    response, err3 := client.Do(request)
    return response, err3
}

/**
 * Send POST /disconnect to the client to request that it clean up and exit.
 * @return the response from the client and any error that occurs
 */
func (c *Client)Disconnect() (*http.Response, error) {
    request, err1 := http.NewRequest("POST", disconnecUrl(c.PortNumber), nil)
    if err1 != nil {
        return nil, err1
    }
    client := &http.Client{}
    response, err2 := client.Do(request)
    return response, err2
}

/**
 * Send POST /prompt to the client to prompt it to send a message to another client.
 * @param to - The identifier of the client the message should be directed at
 * @param message - The content of the message to send
 * @return the response from the client and any error that occurs
 */
func (c *Client)PromptSend(to, message string) (*http.Response, error) {
    data, err1 := json.Marshal(PromptMessage{to, message})
    if err1 != nil {
        return nil, err1
    }
    reader := bytes.NewReader(data)
    request, err2 := http.NewRequest("POST", promptUrl(c.PortNumber), reader)
    if err2 != nil {
        return nil, err2
    }
    request.Header.Set("Content-Type", "application/json")
    client := &http.Client{}
    response, err3 := client.Do(request)
    return response, err3
}

/**
 * Send POST /received to inform the client that it has received a message.
 * @param from - The identifier of the client that sent the message
 * @param message - The content of the message received
 * @return the response from the client and any error that occurs
 */
func (c *Client)Send(from, message string) (*http.Response, error) {
    now = time.Now().Format(time.UnixDate)
    data, err1 := json.Marshal(ReceivedMessage{from, message, now})
    if err1 != nil {
        return nil, err1
    }
    reader := bytes.NewReader(data)
    request, err2 := http.NewRequest("POST", receivedUrl(c.PortNumber), reader)
    if err2 != nil {
        return nil, err2
    }
    request.Header.Set("Content-Type", "application/json")
    client := &http.Client{}
    response, err3 := client.Do(request)
    return response, err3
}

/**
 * The route on which a client expects to be notified it has joined a chat.
 * @param port - The port number the client's HTTP server listens on
 */
func joinedUrl(port string) string {
    return "http://localhost:" + port + "/joined"
}

/**
 * The route on which a client expects to be told to disconnect.
 * @param port - The port number the client's HTTP server listens on
 */
func disconnectUrl(port string) string {
    return "http://localhost:" + port + "/disconnect"
}

/**
 * The route on which a client expects to be prompted to send a message
 * @param port - The port number the client's HTTP server listens on
 */
func disconnectUrl(port string) string {
    return "http://localhost:" + port + "/prompt"
}

/**
 * The route on which a client expects to be informed that it has received a message
 * @param port - The port number the client's HTTP server listens on
 */
func disconnectUrl(port string) string {
    return "http://localhost:" + port + "/received"
}
