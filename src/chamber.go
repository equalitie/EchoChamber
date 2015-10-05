package main

import (
	"fmt"
	"net/http"
    "encoding/json"
    "github.com/gorilla/mux"
)

/**
 * Holds a decoded request for a message to be sent to another client
 */
type SendMessageRequest struct {
    Message string `json: "message"`
    Recipient string `json: "to"`
}

/**
 * A direct analogue of SendMessageRequest, but with a slightly different
 * "from" field. Meant to be sent to recipient clients.
 */
type ReceivedMessage struct {
    Message string `json: "message"`
    From string `json: "from"`
}

/**
 * Holds a response to a send-message request
 */
type SendMessageResponse struct {
    Success bool `json: "success"`
    QueueIndex int `json: "queueIndex"`
}

/**
 * Temporary placeholder
 */
func helloWorld(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte("Hello world!"))
}

/**
 * Handle a request to have a message sent to another client.
 */
func sendMessage(w http.ResponseWriter, r *http.Request) {
    fmt.Println("Asked to send message")
    decoder := json.NewDecoder(r.Body)
    sendMsgReq := SendMessageRequest{}
    decodeErr := decoder.Decode(&sendMsgReq)
    if decodeErr != nil {
        fmt.Println("Could not parse message")
        w.Write([]byte("{\"success\": false, \"queueIndex\": -1}"))
    } else {
        fmt.Pritnln(sendMsgreq)
        w.Write([]byte("{\"success\": true, \"queueIndex\": 0}"))
    }
    // TODO - Delete this!
    // Act like an echo server and send back whatever we received
    sendErr := notifyReceived(sendMsgReq)
    if sendErr != nil {
        fmt.Println("Echoed message")
    } else {
        fmt.Pritnln("Could not echo")
        fmt.Println(sendErr)
    }
}

/**
 * Notify a client that a message has been received for it.
 * @param smr - The message requested to be sent
 * @return an error if one occurs
 */
func notifyReceived(smr SendMessageRequest) error {
    data, _ := json.Marshal(ReceivedMessage{smr.Message, "abc123"}) // Fake sender ID
    reader bytes.NewReader(data)
    // TODO - Keep a table of participating clients to find the appropriate send URL
    req, err := http.NewRequest("POST", "http://localhost:9005", reader)
    if err != nil {
        return err
    }
    req.Header().Set("Content-Type", "application/json")
    client := &http.Client{}
    _, err2 := client.Do(req)
    return err2
}

func main() {
    router := mux.NewRouter()
    router.HandleFunc("/", helloWorld)
    router.HandleFunc("/send", sendMessage).Methods("POST")
    http.Handle("/", router)
    // TODO - Make this configurable
	http.ListenAndServe(":9004", nil)
	fmt.Println("Listening on localhost:9004")
}
