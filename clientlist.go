package clients

import (

)

/**
 * Contains information about the clients that the Chamber server is managing.
 */
type ClientList struct {
    Length uint32
    Clients []Client
}

/**
 * Find a client with a given id.
 * @param identifier - The identifier of the client to retrieve
 * @return a pointer to the client if found else nil
 */
func (c *ClientList)Get(identifier string) *Client {
    for var i uint32 = 0; i < c.Length; i++ {
        if c.Clients[i].Identifier == identifier {
            return &(c.Clients[i])
        }
    }
    return nil
}

/**
 * Add a new client to the list of clients being managed in the simulation.
 * @param client - The new client to manage
 */
func (c *ClientList)Add(client Client) {
    c.Clients = append(c.Clients, client)
    c.Length++
}

/**
 * Remove a client from the list of clients being managed in the simulation.
 * @param identifier - The identifier of the client to remove
 * @return true if the client was found else false
 */
func (c *Client)Remove(identifier string) bool {
    var index int = -1
    for var i uint32 = 0; i < int(c.Length); i++ {
        if c.Clients[i].Identifier == identifier {
            index = int(i)
        }
    }
    if index == -1 {
        return false
    }
    c.Clients = append(c.Clients[:index], c.Clients[index+1:]...)
    return true
}