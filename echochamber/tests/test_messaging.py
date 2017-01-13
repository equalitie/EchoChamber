"""
Test client connections to a XMPP chat room
"""
import math
import time
import bisect
import logging
import random
import Queue
from threading import Thread

import pytest

from echochamber.utils import create_client_connections, establish_channel, find_available_port
from echochamber.proxy import ProxyServer


def read_messages(clients, counters, timeout):
    def run(client, queue):
        now = time.time()
        start = now
        read = 0
        while (start + timeout) > now:
            try:
                client.read_message(timeout)
                read += 1
                now = time.time()
            except Exception:
                break

        queue.put(read)

    threads = []

    for client in clients:
        username = client.username
        q = Queue.Queue()
        t = Thread(target=run, args=(client, q))
        t.start()
        threads.append((t, q, username))

    for t, q, username in threads:
        t.join()
        counters[username] += q.get()


def read_rest_of_messages(clients, counters, total):
    def run(client, so_far):
        while so_far < total:
            try:
                client.read_message(60)
                so_far += 1
            except Exception:
                logging.info("e >>> %s %d %d", client.username, so_far, total)
                assert False

    threads = []

    for client in clients:
        t = Thread(target=run, args=(client, counters[client.username]))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


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
            # For some reason if we only start to read the messages once we sent them all the
            # pexpect library won't read them all back. But if we read _some_ of them while we're
            # waiting until the time the next message is to be sent, then we greatly increase the
            # chances pexpect will read them all. Unfotunately, it's still not bullet proof and
            # then big tests with 25 or more nodes still fail because few messages are not
            # received. I (github/inetic) have checked the logs from each client and the
            # messages are actually received fine by jabberite but are lost somewhere
            # in the pexpect library before they are read.
            read_messages(clients, recv_count, send_at - elapsed)
            # If you want to try not to read messages here, just replace the above line with
            # time.sleep(send_at - elapsed)

    logging.info("Finished sending %d messages", total_messages)

    # Wait for all messages to arrive
    # NOTE: Reading from all clients at once also seems to increase chances
    #       of receiving all the messages from pexpect for some reason.
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
