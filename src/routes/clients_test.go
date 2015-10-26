package routes

import (
	"../clients"
	"bytes"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strconv"
	"strings"
	"testing"
)

func getPort(URL string) int {
	parsed, _ := url.Parse(URL)
	parts := strings.Split(parsed.Host, ":")
	port, _ := strconv.Atoi(parts[1])
	return port
}

func createClient(chamberPort int, identifier string, participants []string) error {
	marshalled, marshalErr := json.Marshal(CreateClientParam{identifier, participants})
	if marshalErr != nil {
		return marshalErr
	}
	reader := bytes.NewReader(marshalled)
	url := "http://localhost:" + strconv.Itoa(chamberPort) + "/clients"
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
	url := "http://localhost:" + strconv.Itoa(getPort(testServer.URL)) + "/clients"
	request, reqErr := http.NewRequest("POST", url, reader)
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
	foundClient := cl.Get("testing1")
	if foundClient == nil {
		t.Error("Could not get client1")
	} else {
		foundClient.Disconnect()
	}
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
	reader := bytes.NewReader(data)
	url := "http://localhost:" + strconv.Itoa(getPort(testServer.URL)) + "/clients/disconnect"
	request, reqErr := http.NewRequest("POST", url, reader)
	if reqErr != nil {
		t.Error(reqErr.Error())
	}
	client := http.Client{}
	response, err := client.Do(request)
	if err != nil {
		t.Error(err.Error())
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
	reader := bytes.NewReader(data)
	url := "http://localhost:" + strconv.Itoa(getPort(testServer.URL)) + "/clients/prompt"
	request, reqErr := http.NewRequest("POST", url, reader)
	if reqErr != nil {
		t.Error(reqErr.Error())
	}
	client := http.Client{}
	response, err := client.Do(request)
	if err != nil {
		t.Error(err.Error())
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
	foundClient1 := cl.Get("testing3")
	foundClient2 := cl.Get("testing4")
	if foundClient1 == nil {
		t.Error("Could not find client testing3")
	} else if foundClient2 == nil {
		t.Error("Could not find client testing4")
	} else {
		foundClient1.Disconnect()
		foundClient2.Disconnect()
	}
	cl.Remove("testing3")
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
	reader := bytes.NewReader(data)
	url := "http://localhost:" + strconv.Itoa(getPort(testServer.URL)) + "/clients/send"
	request, reqErr := http.NewRequest("POST", url, reader)
	if reqErr != nil {
		t.Error(reqErr.Error())
	}
	client := http.Client{}
	response, err := client.Do(request)
	if err != nil {
		t.Error(err.Error())
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
	foundClient1 := cl.Get("testing5")
	foundClient2 := cl.Get("testing6")
	if foundClient1 == nil {
		t.Error("Could not find client testing5")
	} else if foundClient2 == nil {
		t.Error("Could not find client testing6")
	} else {
		foundClient1.Disconnect()
		foundClient2.Disconnect()
	}
	cl.Remove("testing5")
	cl.Remove("testing6")
}
