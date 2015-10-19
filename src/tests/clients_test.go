package main

import (
    "testing"
    "strings"
    "net/http"
    "net/http/httptest"
    "encoding/json"
)

func TestNotifyJoined(t *testing.T) {
    testClient := NewClient("", "testing1", "9010")
    testServer := httptest.NewUnstartedServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !strings.HasSuffix(r.URL.String(), "/joined") {
            t.Error("Got request for an endpoint other than /joined")
            w.Write([]byte("Got request for an endpoint other than /joined"))
            return
        }
        if r.Method != "POST" {
            t.Error("Request to /joined is not a POST request")
            w.Write([]byte("Request to /joined is not a POST request"))
            return
        }
        decoder := json.NewDecoder(r.Body)
        joinedMsg := JoinedMessage{}
        decodeErr := decoder.Decode(&joinedMsg)
        if decodeErr != nil {
            t.Error(decodeErr.Error())
            w.Write([]byte(decodeErr.Error()))
            return
        }
        if joinedMsg.Id != "testing1" || joinedMsg.Participants[0] != "participant1" {
            t.Error("Did not get expected values in message.")
            w.Write([]byte("Did not get expected values in message."))
        } else {
            w.Write([]byte("Success!"))
        }
    }))
    testServer.URL = "http://localhost:9010"
    testServer.Start()
    defer testServer.Close()
    _, err := testClient.NotifyJoined([...]string{"participant1", "participant2"})
    if err != nil {
        t.Error(err.Error())
    }
}

func TestDisconnect(t *testing.T) {
    testClient := NewClient("", "testing2", "9010")
    testServer := httptest.NewUnstartedServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !strings.HasSuffix(r.URL.String(), "/disconnect") {
            t.Error("Got request for an endpoint other than /disconnect")
            w.Write([]byte("Got request for an endpoint other than /disconnect"))
            return
        }
        if r.Method != "POST" {
            t.Error("Request to /disconnect is not a POST request. Got " + r.Method)
            w.Write([]byte("Request to /disconnect is not a POST request. Got " + r.Method))
            return
        }
        w.Write([]byte("Success!"))
    }))
    testServer.URL = "http://localhost:9010"
    testServer.Start()
    defer testServer.Close()
    _, err := testClient.Disconnect()
    if err != nil {
        t.Error(err.Error())
    }
}

func TestPromptSend(t *testing.T) {
    testClient := NewClient("", "testing3", "9010")
    testServer := httptest.NewUnstartedServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !strings.HasSuffix(r.URL.String(), "/prompt") {
            t.Error("Got request for an endpoint other than /prompt. Got " + r.URL.String())
            w.Write([]byte("Got request for an endpoint other than /prompt. Got " + r.URL.String()))
            return
        }
        if r.Method != "POST" {
            t.Error("Request to /prompt is not a POST request. Got " + r.Method)
            w.Write([]byte("Request to /prompt is not a POST request. Got " + r.Method))
            return
        }
        promptMsg := PromptMessage{}
        decoder := json.NewDecoder(r.Body)
        decodeErr := decoder.Decode(&promptMsg)
        if decodeErr != nil {
            t.Error(decodeErr.Error())
            w.Write([]byte(decodeErr.Error()))
            return
        }
        if promptMsg.From != "testing3" {
            t.Error("Prompt message did not come from testing3. Came from " + promptMsg.From)
            w.Write([]byte("Prompt message did not come from testing3. Came from " + promptMsg.From))
        } else if promptMsg.Message != "Hello world!" {
            t.Error("Prompt message did not contain expected message. Got "+ promptMsg.Message)
            w.Write([]byte("Prompt message did not contain expected message. Got "+ promptMsg.Message))
        } else if promptMsg.To != "testServer" {
            t.Error("Prompt message is not directed at testServer. Directed at " + promptMsg.To)
            w.Write([]byte("Prompt message is not directed at testServer. Directed at " + promptMsg.To))
        } else {
            w.Write([]byte("Success!"))
        }
    }))
    testServer.URL = "http://localhost:9010"
    testServer.Start()
    defer testServer.Close()
    _, err := testClient.PromptSend("testServer", "Hello world!")
    if err != nil {
        t.Error(err.Error())
    }
}

func TestNotifyReceived(t *testing.T) {
    testClient := NewClient("", "testing4", "9010")
    testServer := httptest.NewUnstartedServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !strings.HasSuffix(r.URL.String(), "/received") {
            t.Error("Got request for an endpoint other than /received. Got " + r.URL.String())
            w.Write([]byte("Got request for an endpoint other than /received. Got " + r.URL.String()))
            return
        }
        if r.Method != "POST" {
            .Error("Request to /received is not a POST request. Got " + r.Method)
            w.Write([]byte("Request to /received is not a POST request. Got " + r.Method))
            return
        }
        sendMsg := ReceievedMessage{}
        decoder := json.NewDecoder(r.Body)
        decodeErr := decoder.Decode(&sendMsg)
        if decodeErr != nil {
            t.Error(decodeErr.Error())
            w.Write([]byte(decodeErr.Error()))
            return
        }
        if sendMsg.From != "testServer" {
            t.Error("Received message did not come from testServer. Came from " + sendMsg.From)
            w.Write([]byte("Received message did not come from testServer. Came from " + sendMsg.From))
        } else if sendMsg.Message != "Hello world!" {
            t.Error("Received message did not contain expected message. Got " + sendMsg.Message)
            w.Write([]byte("Received message did not contain expected message. Got " + sendMsg.Message))
        } else {
            w.Write([]byte("Success!"))
        }
    }))
    testServer.URL = "http://localhost:9010"
    testServer.Start()
    defer testServer.Close()
    _, err := testClient.NotifyReceived("testServer", "Helo world!", time.Now().Format(time.UnixDate))
    if err != nil {
        t.Error(err.Error())
    }
}
