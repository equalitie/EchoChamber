package routes

import (
    "../clients"
    "net/http"
    "fmt"
)

func CreateClient(cl *clients.ClientList) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
    }
}

func DisconnectClient(cl *clients.ClientList) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {

    }
}

func PromptClient(cl *clients.ClientList) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
    }
}


func SendToClient(cl *clients.ClientList) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
    }
}
