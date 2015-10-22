package clients

import (
    "fmt"
)

/**
 * Contains information about the clients that the Chamber server is managing.
 */
type ClientList struct {
    Length uint32
    Clients []Client
    Command string
    Arguments []string
    NextPort int
}

/**
 * Create a new client list with no clients in it.
 * @param firstPort - The first port number to prescribe to a client
 * @param command - The program to run to start the client
 * @param args - Any arguments to pass to the program
 */
func NewClientList(firstPort int, command string, args ...string) ClientList {
    clients := make([]Client, 0)
    return ClientList{0, clients, command, args, firstPort}
}

/**
 * Find a client with a given id.
 * @param identifier - The identifier of the client to retrieve
 * @return a pointer to the client if found else nil
 */
func (c *ClientList)Get(identifier string) *Client {
    var i uint32
    for i = 0; i < c.Length; i++ {
        if c.Clients[i].Identifier == identifier {
            fmt.Printf("Found %s at index %d\n", identifier, i)
            return &(c.Clients[i])
        }
    }
    return nil
}

/**
 * Add a new client to the list of clients being managed in the simulation.
 * @param identifier - The identifier to prescribe to the new client
 */
func (c *ClientList)Add(identifier string) (Client, error) {
    client := NewClient(c.Command, identifier, c.NextPort)
    startErr := client.Start(c.Arguments...)
    if startErr != nil {
        return nil, startErr
    }
    participants := make([]string, c.Length)
    for i, participant := range c.Clients {
        participants[i] = participant.Identifier
    }
    // TODO - Come up with a more clever way to deal with the client's responses
    _, err := client.NotifyJoined(participants)
    if err != nil {
        client.Disconnect()
        return nil, err
    }
    c.Clients = append(c.Clients, client)
    c.Length++
    c.NextPort++
    return client, nil
}

/**
 * Remove a client from the list of clients being managed in the simulation.
 * @param identifier - The identifier of the client to remove
 * @return true if the client was found else false
 */
func (c *ClientList)Remove(identifier string) bool {
    var index int = -1
    var i uint32
    for i = 0; i < c.Length; i++ {
        if c.Clients[i].Identifier == identifier {
            index = int(i)
        }
    }
    if index == -1 {
        return false
    }
    // TODO - Again we should probably do something with the return values here
    c.Clients[i].Disconnect()
    c.Clients = append(c.Clients[:index], c.Clients[index+1:]...)
    c.Length--
    return true
}
