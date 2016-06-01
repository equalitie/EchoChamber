package routes

import (
	"../clients"
	"encoding/json"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
)

/**
 * Set the content type of a response to application/json
 */
func SetJsonCT(w *http.ResponseWriter) {
	(*w).Header().Set("Content-Type", "application/json")
}

/**
 * Write a response to the client informing them that their recent command was
 * not successful.
 * @param w - The response writer through which the client can be reached
 * @param errMsg - A message explaining what caused the failure
 */
func WriteFailure(w http.ResponseWriter, errMsg string) {
	marshalled, _ := json.Marshal(GeneralFailure{false, errMsg})
	w.Write(marshalled)
}

/**
 * A super-simple placeholder route
 */
func HelloWorld(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte("Hello world!"))
}

func InitClientHandlers(router *mux.Router, cl *clients.ClientList) {
	fmt.Println("Calling InitClientHandlers")
	router.HandleFunc("/", CreateClient(cl))
}
