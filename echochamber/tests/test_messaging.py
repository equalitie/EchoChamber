"""
Test client connections to a XMPP chat room
"""
import math
import time
import bisect
import logging
import random
from threading import Thread

import pytest

from echochamber.utils import create_client_connections, establish_channel, find_available_port
from echochamber.proxy import ProxyServer


def read_messages(clients, counters, timeout):
    def run(client):
        now = time.time()
        end = now + timeout
        while now < end:
            try:
                client.read_message(end - now)
                counters[client.username] += 1
                now = time.time()
            except Exception:
                break

    threads = []

    for client in clients:
        t = Thread(target=run, args=(client,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def read_rest_of_messages(clients, counters, total):
    def run(client):
        while counters[client.username] < total:
            try:
                client.read_message(5*60)
                counters[client.username] += 1
            except Exception:
                break

    threads = []

    for client in clients:
        username = client.username
        t = Thread(target=run, args=(client,))
        t.start()
        threads.append((t, username))

    success = True

    for t, username in threads:
        logging.info("Joining %s", username)
        t.join()

        messages_read = counters[username]

        if messages_read != total:
            success = False
            logging.info("Client %s read only %d out of %d messages",
                         username, messages_read, total)

    assert success


def connect_and_send_messages(client_factory, debug, num_clients, server_port=None):
    total_time = 200  # Time period for sending all messages
    frequency_high = 0.60  # 6 messages every 10 seconds
    frequency_low = 0.10  # 1 message every 10 seconds
    # threshhold = 300
    percentage_high_users = 0.1

    # Join all clients to the room
    clients = create_client_connections(client_factory, num_clients, proxy_port=server_port)
    establish_channel(clients)
    logging.info("All clients have been invited to the channel, sending message tests")

    num_high_users = int(math.ceil(num_clients * percentage_high_users))
    high_users, low_users = clients[0:num_high_users], clients[num_high_users:]

    logging.info("Chose %d high frequency messaging users and %d low frequency users.",
                 len(high_users), len(low_users))

    message_queue = []
    for client in clients:
        if client in high_users:
            msg_freq = frequency_high
        else:
            msg_freq = frequency_low

        num_messages = int(total_time * msg_freq)

        # Schedule each message to be sent by this client
        for i in range(num_messages):
            # Pick a random time in the total_time range to send the message
            # bisect.insort will queue messages in the list ordered by scheduled time
            queued_time = random.uniform(0, total_time)
            bisect.insort_right(message_queue, (queued_time, client))

    # Run a loop and send all queued messages at the schedule times
    start_time = time.time()
    message_id = 0
    total_messages = len(message_queue)

    ids = {}
    recv_count = {}
    for client in clients:
        ids[client.username] = 0
        recv_count[client.username] = 0

    while message_queue:
        # Check if first message is ready to be sent (we have reached the scheduled send time)
        elapsed = time.time() - start_time
        send_at = message_queue[0][0]

        if elapsed >= send_at:
            queued_time, client = message_queue.pop(0)
            message_id += 1
            logging.info("Sending message %d for %s queued at %0.2f",
                         message_id, client.username, queued_time)

            client.send_message("{message_id} {time:0.2f} {username} {mid}".format(
                message_id=message_id,
                time=queued_time,
                username=client.username,
                mid=ids[client.username])
            )
            ids[client.username] += 1
        else:
            # Interestingly, using `time.sleep(send_at - elapsed)` here
            # instead of read_messages will make the 10 node test pass
            # on our Xeon test server while when read_messages is used
            # the test fails. But when it fails and the log of each client
            # is inspected it can be seen that all messages are actually
            # received by jabberites. On the other hand, the 25 node test
            # fail in both cases (when time.sleep and read_messages is
            # used) but when read_messages is used, it can again be shown
            # from the logs that all messages are actually received by
            # jabberites but are lost somewhere in the pexpect library.
            read_messages(clients, recv_count, send_at - elapsed)
            # time.sleep(send_at - elapsed)

    logging.info("Finished sending %d messages", total_messages)

    # Wait for all messages to arrive
    # NOTE: Reading from all clients at once seems to increase chances
    #       of receiving all the messages from pexpect.
    read_rest_of_messages(clients, recv_count, total_messages)

    logging.info("All clients received all sent messages")


@pytest.mark.parametrize("num_clients", [
    10,
    pytest.mark.skipif("os.environ.get('CI', None)")(25),
])
def test_messaging(client_factory, debug, num_clients):
    """
    Test that clients connect and can send varying number of messages
    """
    connect_and_send_messages(client_factory, debug, num_clients)


@pytest.mark.parametrize("num_clients", [
    10,
    pytest.mark.skipif("os.environ.get('CI', None)")(25),
])
def test_messaging_high_latency(xmpp_server, client_factory, debug, num_clients):
    """
    Connect all clients via the latency proxy server
    """
    latency_mean = 0.2
    latency_variance = 0.025
    proxy_port = find_available_port()
    proxy = ProxyServer(("127.0.0.1", proxy_port), ("127.0.0.1", xmpp_server.c2s_port),
                        latency_mean, latency_variance)
    logging.info("Proxy listening on port {} with latency mean {}s and variance {}s".
                 format(proxy_port, latency_mean, latency_variance))

    # Join all clients to the room via a high-latency proxy
    connect_and_send_messages(client_factory, debug, num_clients, server_port=proxy_port)

    proxy.stop()
