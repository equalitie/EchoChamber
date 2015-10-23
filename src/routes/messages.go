/**
 * Defined within this file are data types that endpoint arguments
 * (provided as JSON) can be decoded into and marshalled from.
 *
 * Structures for containing data decoded from JSON paramters in requests
 * are suffixed with "Param" and structures for containing data for
 * responses are suffixed with "Resp".
 */

package routes

/**
 * Message written in the general error case to inform the client of failure.
 */
type GeneralFailure struct {
	Success bool   `json:"success"`
	Reason  string `json:"reason"`
}

/**
 * Message written in the case that a message could not be sent.
 */
type SendMessageFailure struct {
	Success    bool   `json:"success"`
	Dropped    bool   `json:"dropped"`
	Reason     string `json:"reason"`
	QueueIndex int    `json:"queueIndex"`
}

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
