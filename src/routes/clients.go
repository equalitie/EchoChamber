package routes

import (
    "net/http"
    "fmt"
)

func CreateClient(w http.ResponseWriter, r *http.Request) {
    fmt.Println("Got a request to create a new client")
    w.Write([]byte("Hello world!"))
}
