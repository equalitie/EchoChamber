package routes

import (
    "net/http"
    "github.com/gorilla/mux"
)

/**
 * A super-simple placeholder route
 */
func HelloWorld(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/plain")
    w.Write([]byte("Hello world!"))
}

func InitClientHandlers(router *mux.Router) {
    router.HandleFunc("/", CreateClient)
}
