package main

import (
	"./clients"
	"./routes"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
)

func main() {
	clientList := clients.NewClientList()
	router := mux.NewRouter()
	router.HandleFunc("/", routes.HelloWorld)
	clientsRouter := router.PathPrefix("/client").Subrouter()
	routes.InitClientHandlers(clientsRouter, &clientList) // , &clientList)
	http.Handle("/", router)
	// TODO - Make this configurable
	fmt.Println("Listening on localhost:9004")
	http.ListenAndServe(":9004", nil)
}
