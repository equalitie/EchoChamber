/**
 * Defined within this file are data types that endpoint arguments
 * (provided as JSON) can be decoded into and marshalled from.
 *
 * Structures for containing data decoded from JSON paramters in requests
 * are suffixed with "Param" and structures for containing data for
 * responses are suffixed with "Resp".
 */

package routes

type CreateClientParam struct {
	Identifier   string   `json:"id"`
	Participants []string `json:"participants"`
}

type CreateClientResp struct {
	Success bool `json:"success"`
}

type DisconnectClientParam struct {
	Identifier string `json:"id"`
}

type DisconnectClientResp struct {
	Success bool `json:"success"`
}

type PromptClientParam struct {
	From    string `json:"from"`
	To      string `json:"to"`
	Message string `json:"message"`
}

type PromptClientResp struct {
	Success bool `json:"success"`
}

type SendClientParam struct {
	From    string `json:"myId"`
	To      string `json:"to"`
	Message string `json:"message"`
}

type SendClientResp struct {
	Success    bool `json:"success"`
	QueueIndex int  `json:"queueIndex"`
	Dropped    bool `json:"dropped"`
}
