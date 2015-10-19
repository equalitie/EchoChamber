package main

/**
 * The contents of a message sent to inform a client it has joined the simulation.
 */
type JoinedMessage struct {
	Id           string   `json:"id"`
	Participants []string `json:"participants"`
}

/**
 * The contents of a message sent to prompt a client to send a message.
 */
type PromptMessage struct {
	From    string `json:"from"`
	To      string `json:"to"`
	Message string `json:"message"`
}

/**
 * The contents of a message sent to inform a client it has received a message.
 */
type ReceivedMessage struct {
	From    string `json:"from"`
	Message string `json:"message"`
	Date    string `json:"date"`
}

/**
 * Holds a decoded request for a message to be sent to another client
 */
type SendMessageRequest struct {
	Message   string `json:"message"`
	From      string `json:"myId"`
	Recipient string `json:"to"`
}

/**
 * Holds a response to a send-message request
 */
type SendMessageResponse struct {
	Success    bool `json:"success"`
	QueueIndex int  `json:"queueIndex"`
}
