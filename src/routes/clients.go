/**
 * This file contains middleware for building handlers for routes
 * prefixed with /client, used for managing the list of clients and
 * having messages sent between them.
 *
 * TODO
 * - Right now, messages are being immediately sent between clients, but we want
 *   to send them to the test environment first
 */

package routes

import (
	"../clients"
	"encoding/json"
	"net/http"
	"time"
)

const COULD_NOT_FIND string = "Could not find any client with identifier "

/**
 * Create a handler for requests to have a new client created.
 * @param cl - The client list that is shared between all client handlers
 */
func CreateClient(cl *clients.ClientList) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		SetJsonCT(&w)
		ccp := CreateClientParam{}
		decoder := json.NewDecoder(r.Body)
		decodeErr := decoder.Decode(&ccp)
		if decodeErr != nil {
			WriteFailure(w, decodeErr.Error())
		} else {
			// TODO - Get the command and arguments from a configuration object
			newClient := clients.NewClient("python", ccp.Identifier, cl.NextPort())
			startErr := newClient.Start("examples/basic_client.py")
			if startErr != nil {
				WriteFailure(w, startErr.Error())
				return
			}
			// TODO - Perhaps we should do something with the response
			_, notifyErr := newClient.NotifyJoined(ccp.Participants)
			if notifyErr != nil {
				WriteFailure(w, notifyErr.Error())
				return
			}
			marshalled, _ := json.Marshal(CreateClientResp{true})
			w.Write(marshalled)
			cl.Add(newClient)
		}
	}
}

/**
 * Create a handler for requests to have a client disconnected.
 * @param cl - The client list that is shared between all client handlers
 */
func DisconnectClient(cl *clients.ClientList) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		SetJsonCT(&w)
		dcp := DisconnectClientParam{}
		decoder := json.NewDecoder(r.Body)
		decodeErr := decoder.Decode(&dcp)
		if decodeErr != nil {
			WriteFailure(w, decodeErr.Error())
		} else {
			client := cl.Get(dcp.Identifier)
			if client == nil {
				WriteFailure(w, COULD_NOT_FIND+dcp.Identifier)
				return
			}
			// TODO - We should really do something with these responses
			_, disconErr := client.Disconnect()
			if disconErr != nil {
				WriteFailure(w, disconErr.Error())
				return
			}
			marshalled, _ := json.Marshal(DisconnectClientResp{true})
			w.Write(marshalled)
			cl.Remove(dcp.Identifier)
		}
	}
}

/**
 * Create a handler for requests to have a client prompted to send a message.
 * @param cl - The client list that is shared between all client handlers
 */
func PromptClient(cl *clients.ClientList) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		SetJsonCT(&w)
		pcp := PromptClientParam{}
		decoder := json.NewDecoder(r.Body)
		decodeErr := decoder.Decode(&pcp)
		if decodeErr != nil {
			WriteFailure(w, decodeErr.Error())
		} else {
			client := cl.Get(pcp.From)
			if client == nil {
				WriteFailure(w, COULD_NOT_FIND+pcp.From)
				return
			}
			if cl.Get(pcp.To) == nil {
				WriteFailure(w, COULD_NOT_FIND+pcp.To)
				return
			}
			// TODO - Handle response
			_, promptErr := client.PromptSend(pcp.To, pcp.Message)
			if promptErr != nil {
				WriteFailure(w, promptErr.Error())
				return
			}
			marshalled, _ := json.Marshal(PromptClientResp{true})
			w.Write(marshalled)
		}
	}
}

/**
 * Create a handler for requests to have a client send a message.
 * @param cl - The client list that is shared between all client handlers
 */
func SendToClient(cl *clients.ClientList) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		SetJsonCT(&w)
		scp := SendClientParam{}
		decoder := json.NewDecoder(r.Body)
		decodeErr := decoder.Decode(&scp)
		if decodeErr != nil {
			WriteFailure(w, decodeErr.Error())
		} else {
			client := cl.Get(scp.To)
			if client == nil {
				WriteFailure(w, COULD_NOT_FIND+scp.To)
				return
			}
			if cl.Get(scp.From) == nil {
				WriteFailure(w, COULD_NOT_FIND+scp.From)
				return
			}
			now := time.Now().Format(time.UnixDate)
			_, sendErr := client.NotifyReceived(scp.From, scp.Message, now)
			if sendErr != nil {
				WriteFailure(w, sendErr.Error())
				return
			}
			marshalled, _ := json.Marshal(SendClientResp{true, 0, false})
			w.Write(marshalled)
		}
	}
}
