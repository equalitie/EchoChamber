package routes

import (
	"../clients"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
)

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
