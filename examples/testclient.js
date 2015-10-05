"use strict";

let http = require('http');
let url = require('url');
let request = require('request');
let concatStream = require('concat-stream');

const SEND_URL = 'http://localhost:9004/send';

/**
 * Send a message to the Chamber server and log the response it sends us.
 * @param {string} message - The message to send
 * @param {string} id - The identifier of the client we want to send to
 */
function sendMessage(message, to) {
    request({
        url: SEND_URL,
        method: 'POST',
        json: true,
        body: {
            message: message,
            to: to
        },
        headers: {
            'Content-Type': 'application/json'
        }
    }, (err, response, body) => {
        if (err) {
            console.log('Failed to send messsage!');
            console.log(err);
        } else {
            console.log(
                'Response to send request:\n\tSuccess:', body.success, 
                '\n\tQueue Index:', body.queueIndex);
        }
    });
}

/**
 * Read all the data being POSTed to us and invoke a callback with any error that might
 * occur or the streamed body contents.
 * @param {http.IncomingMessage} req - The request received by our HTTP server, wrapping our "client"
 * @param {function} callback - A function to invoke when we finish obtaining the body or have an error
 */
function handleBody(req, callback) {
  req.on('error', function (err) {
    callback(err, null);
  });
  var concat = concatStream(function (data) {
    callback(null, data);
  });
  req.pipe(concat);
}

/**
 * Run an HTTP server that will listen for messages on the route /received.
 * When a message is received, we can parse it and push it to our actual "client".
 */
let server = http.createServer((req, res) => {
    if (url.parse(req.url).path === '/received') {
        handleBody(req, (err, body) => {
            if (err) {
                console.log('Couldn\'t read POST body\n', err);
            } else {
                console.log('Got a message!');
                console.log(body.toString());
            }
            res.write('Thanks!');   
            res.end();
            server.close();
        });
    } else {
        console.log('Got an unknown request for', req.url);
        res.write('What?');
        res.end();
    }
});

server.listen(9005);
console.log('Listening on port 9005');

// Send a message to chamber to get the test started
sendMessage('Hello, world!', 'myself');
