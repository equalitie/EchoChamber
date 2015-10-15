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
