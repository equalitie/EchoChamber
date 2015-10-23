package routes

import (
    "../clients"
    "testing"
    "encoding/json"
    "bytes"
    "errors"
    "strings"
    "net/http"
    "net/http/httptest"
)

func getPort(URL string) string {
	parsed, _ := url.Parse(URL)
	parts := strings.Split(parsed.Host, ":")
	return parts[1]
}

func createClient(chamberPort, identifier string, participants []string) error {
    marshalled, marshalErr := json.Marshal(CreateClientParam{identifier, participants})
    if marshalErr != nil {
        return marshalErr
    }
    reader := bytes.NewReader(marshalled)
    url := "http://localhost:" + chamberPort + "/clients"
    request, reqErr := http.NewRequest("POST", url, reader)
    if reqErr != nil {
        return reqErr
    }
    client := &http.Client{}
    response, err := client.Do(request)
    if err != nil {
        return err
    }
    decoder := json.NewDecoder(response.Body)
    defer response.Body.Close()
    ccr := CreateClientResp{}
    decodeErr := decoder.Decode(&ccr)
    if decodeErr != nil {
        return decodeErr
    } else if ccr.Success == false {
        return errors.New("Did not succeed at creating a client")
    }
    return nil
}

// TODO - don't rely on the create client running the basic_client python script
func TestCreateClient(t *testing.T) {
    cl := clients.NewClientList()
    testServer := httptest.NewServer(http.HandlerFunc(CreateClient(&cl)))
    // Start by actually setting up the client
    participants := make([]string, 0)
    data, marshalErr := json.Marshal(CreateClientParam{"testing1", participants})
    if marshalErr != nil {
        t.Error(marshalErr.Error())
    }
    reader := bytes.NewReader(data)
    url := "http://localhost:" + getPort(testServer.URL) + "/clients"
    request, reqErr := http.NewRequest("POST", url , reader)
    if reqErr != nil {
        t.Error(reqErr.Error())
    }
    client := &http.Client{}
    response, err := client.Do(request)
    if err != nil {
        t.Error(err.Error())
    }
    // Ensure that EchoChamber has notified us the creation was successful
    defer response.Body.Close()
    decoder := json.NewDecoder(response.Body)
    ccr := CreateClientResp{}
    decodeErr := decoder.Decode(&ccr)
    if decodeErr != nil {
        t.Error(decodeErr.Error())
    }
    if !ccr.Success {
        t.Error("Client creation ended in failure")
    }
    // End the test by shutting down (hopefully) the client
    cl.Get("testing1").Disconnect()
    cl.Remove("testing1")
}


func TestDisconnectClient(t *testing.T) {
    cl := clients.NewClientList()
    testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if strings.HasSuffix(r.URL.Path, "/disconnect") {
            DisconnectClient(&cl)(w, r)
        } else {
            CreateClient(&cl)(w, r)
        }
    }))
    // Start by actually setting up the client
    participants := make([]string, 0)
    createErr := createClient(getPort(testServer.URL), "testing2", participants)
    if createErr != nil {
        t.Error(createErr.Error())
    }
    // Request that the client be disconnected
    data, marshalErr := json.Marshal(DisconnectClientParam{"testing2"})
    if marshalErr != nil {
        t.Error(marshalErr.Error())
    }
    reader = bytes.NewReader(data)
    url := "http://localhost:" + getPort(testServer.URL) + "/clients/disconnect"
    request, reqErr := http.NewRequest("POST", url, reader)
    if reqErr != nil {
        t.Error(reqErr.Error())
    }
    client = http.Client{}
    response, err := client.Do(request)
    if err != nil {
        t.rror(err.Error())
    }
    // Ensure that EchoChamber has notified us the creation was successful
    defer response.Body.Close()
    decoder := json.NewDecoder(response.Body)
    dcr := DisconnectClientResp{}
    decodeErr := decoder.Decode(&dcr)
    if decodeErr != nil {
        t.Error(decodeErr.Error())
    }
    if !dcr.Success {
        t.Error("Client creation ended in failure")
    }
}

func TestPromptClient(t *testing.T) {
    cl := clients.NewClientList()
    testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if strings.HasSuffix(r.URL.Path, "/prompt") {
            PromptClient(&cl)(w, r)
        } else {
            CreateClient(&cl)(w, r)
        }
    }))
    // Start by actually setting up the client
    participants := make([]string, 0)
    createErr1 := createClient(getPort(testServer.URL), "testing3", participants)
    if createErr1 != nil {
        t.Error(createErr1.Error())
    }
    participants = append(participants, "testing3")
    createErr2 := createClient(getPort(testServer.URL), "testing4", participants)
    if createErr2 != nil {
        t.Error(createErr2.Error())
    }
    // Request that the client be prompted 
    data, marshalErr := json.Marshal(PromptClientParam{"testing3", "testing4", "Hey!"})
    if marshalErr != nil {
        t.Error(marshalErr.Error())
    }
    reader = bytes.NewReader(data)
    url := "http://localhost:" + getPort(testServer.URL) + "/clients/prompt"
    request, reqErr := http.NewRequest("POST", url, reader)
    if reqErr != nil {
        t.Error(reqErr.Error())
    }
    client = http.Client{}
    response, err := client.Do(request)
    if err != nil {
        t.rror(err.Error())
    }
    // Ensure that EchoChamber has notified us the creation was successful
    defer response.Body.Close()
    decoder := json.NewDecoder(response.Body)
    pcr := PromptClientResp{}
    decodeErr := decoder.Decode(&pcr)
    if decodeErr != nil {
        t.Error(decodeErr.Error())
    }
    if !pcr.Success {
        t.Error("Client creation ended in failure")
    }
    cl.Get("testing3").Disconnect()
    cl.Remove("testing3")
    cl.Get("testing4").Disconnect()
    cl.Remove("testing4")
}

func TestSendToClient(t *testing.T) {
    cl := clients.NewClientList()
    testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if strings.HasSuffix(r.URL.Path, "/send") {
            SendToClient(&cl)(w, r)
        } else {
            CreateClient(&cl)(w, r)
        }
    }))
    // Start by actually setting up the client
    participants := make([]string, 0)
    createErr1 := createClient(getPort(testServer.URL), "testing5", participants)
    if createErr1 != nil {
        t.Error(createErr1.Error())
    }
    participants = append(participants, "testing5")
    createErr2 := createClient(getPort(testServer.URL), "testing6", participants)
    if createErr2 != nil {
        t.Error(createErr2.Error())
    }
    // Request that the client be prompted 
    data, marshalErr := json.Marshal(SendClientParam{"testing5", "testing6", "Hey!"})
    if marshalErr != nil {
        t.Error(marshalErr.Error())
    }
    reader = bytes.NewReader(data)
    url := "http://localhost:" + getPort(testServer.URL) + "/clients/send"
    request, reqErr := http.NewRequest("POST", url, reader)
    if reqErr != nil {
        t.Error(reqErr.Error())
    }
    client = http.Client{}
    response, err := client.Do(request)
    if err != nil {
        t.rror(err.Error())
    }
    // Ensure that EchoChamber has notified us the creation was successful
    defer response.Body.Close()
    decoder := json.NewDecoder(response.Body)
    scr := SendClientResp{}
    decodeErr := decoder.Decode(&scr)
    if decodeErr != nil {
        t.Error(decodeErr.Error())
    }
    if !scr.Success {
        t.Error("Client creation ended in failure")
    }
    cl.Get("testing5").Disconnect()
    cl.Remove("testing5")
    cl.Get("testing6").Disconnect()
    cl.Remove("testing6")
}
