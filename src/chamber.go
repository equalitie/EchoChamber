package main

import (
	"./routes"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
)

func main() {
	router := mux.NewRouter()
	router.HandleFunc("/", routes.HelloWorld)
	clientsRouter := router.PathPrefix("/client").Subrouter()
	routes.InitClientHandlers(clientsRouter) // , &clientList)
	http.Handle("/", router)
	// TODO - Make this configurable
	fmt.Println("Listening on localhost:9004")
	http.ListenAndServe(":9004", nil)
}
