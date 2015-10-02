package main

import (
	"fmt"
	"net/http"
)

func helloWorld(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte("Hello world!"))
}

func main() {
	http.HandleFunc("/", helloWorld)
	http.ListenAndServe(":9004", nil)
	fmt.Println("Listening on localhost:9004")
}
