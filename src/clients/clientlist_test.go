package clients

import (
    "testing"
)

func TestGet(t *testing.T) {
    cl := NewClientList()
    // Users of the ClientList type shouldn't append directly.
    cl.Clients = append(cl.Clients, NewClient("", "testing1", "9010"))
    cl.Length++
    var client *Client = cl.Get("testing1")
    if client == nil {
        t.Error("Did not find expected client testing1")
    }
}

func TestAdd(t *testing.T) {
    cl := NewClientList()
    cl.Add(NewClient("", "testing2", "9010"))
    if cl.Length != 1 {
        t.Error("Client list's length was not incremented after adding new client.")
    } else if cl.Clients[0].Identifier != "testing2" {
        t.Error("First client does not have the identifier of the newly added client.")
    }
}

func TestRemove(t *testing.T) {
    cl := NewClientList()
    cl.Clients = append(cl.Clients, NewClient("", "testing3", "9010"))
    cl.Length++
    if !cl.Remove("testing3") {
        t.Error("Failed to find newly inserted client testing3 for removal")
    } else if cl.Length != 0 {
        t.Error("Client list's length was not decremented after removing client.")
    } else if len(cl.Clients) != 0 {
        t.Error("Client list did not actually have client removed.")
    }
}
