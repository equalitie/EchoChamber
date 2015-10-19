package main

import (
	"./routes"
	"encoding/json"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
)

/**
 * Handle a request to have a message sent to another client.
 */
func sendMessage(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Asked to send message")
	decoder := json.NewDecoder(r.Body)
	sendMsgReq := SendMessageRequest{}
	decodeErr := decoder.Decode(&sendMsgReq)
	w.Header().Set("Content-Type", "application/json")
	if decodeErr != nil {
		fmt.Println("Could not parse message")
		fmt.Println(decodeErr)
		w.Write([]byte("{\"success\": false, \"queueIndex\": -1}"))
	} else {
		fmt.Println(sendMsgReq)
		// TODO - Actually make a message queue
		w.Write([]byte("{\"success\": true, \"queueIndex\": 0}"))
	}
}

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
