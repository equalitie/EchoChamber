package clients

import (
	"fmt"
)

/**
 * Contains information about the clients that the Chamber server is managing.
 */
type ClientList struct {
	Length  uint32
	Clients []Client
}

/**
 * Create a new client list with no clients in it.
 */
func NewClientList() ClientList {
	clients := make([]Client, 0)
	return ClientList{0, clients}
}

/**
 * Find a client with a given id.
 * @param identifier - The identifier of the client to retrieve
 * @return a pointer to the client if found else nil
 */
func (c *ClientList) Get(identifier string) *Client {
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
 * @param client - The new client to manage
 */
func (c *ClientList) Add(client Client) {
	c.Clients = append(c.Clients, client)
	c.Length++
}

/**
 * Remove a client from the list of clients being managed in the simulation.
 * @param identifier - The identifier of the client to remove
 * @return true if the client was found else false
 */
func (c *ClientList) Remove(identifier string) bool {
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
	c.Clients = append(c.Clients[:index], c.Clients[index+1:]...)
	c.Length--
	return true
}
