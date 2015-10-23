package routes

import (
	"../clients"
	"fmt"
	"net/http"
)

func CreateClient(cl *clients.ClientList) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		fmt.Println("Got a request to create a new client")
		cl.Add(clients.NewClient("", "testing1", "9010"))
		w.Write([]byte("Created client!"))
	}
}
