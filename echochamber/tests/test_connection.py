"""
Test client connections to a XMPP chat room
"""
import sys
import time
import logging

import pytest
import pexpect

from echochamber.utils import create_client_connections


def invite_debug_user_to_conversation(leader, debug_user):
    """
    Helper to invite an external Jabberite client into the test conversation.
    """
    logging.warning("Waiting for debug user {} to connect".format(debug_user.username))
    try:
        leader.expect(r"User joined: {}".format(debug_user.username), timeout=20)
        leader.invite_conversation(debug_user.username)
        logging.warning("User connected. Waiting for them to join the conversation...")
        leader.expect(r"{} joined the chat session".format(debug_user.username), timeout=30)
    except Exception:
        logging.warning("Could not find debug user, skipping")
        pass


@pytest.mark.parametrize("num_clients", [
    2,
    5,
    10,
])
def test_client_connection(client_factory, debug, num_clients):
    """
    Test that clients can connect, joining a conversation and each sending a message

    This test is a basic overall connection and messaging test. In includes extra
    testing interface for external clients to aid in debugging these tests.
    """
    clients = []

    if debug:
        # Create a user which can be connected too with an external Jabberite client
        debug_user = client_factory("debug")

    clients = create_client_connections(client_factory, num_clients, "connection-test")

    # The first client is designated as the leader, they create the conversation
    # and invite all other users into it.
    leader, clients = clients[0], clients[1:]

    # Start a new np1sec conversation
    time_start = time.time()
    logging.info("Starting connection timer")

    conversation_id = leader.create_conversation()
    leader.select_conversation(conversation_id)
    logging.info("Created and selected conversation %d", conversation_id)

    # Invite all the other users and get each of them to join the conversation.
    for client in clients:
        leader.invite_and_join_conversation(client)

    logging.info("Starting conversation with %d participants took %0.2f seconds",
                 num_clients, time.time() - time_start)
    logging.info("All clients have been invited to the channel, sending message tests")

    if debug:
        invite_debug_user_to_conversation(leader, debug_user)

    # Perform a basic messaging test
    # Send a message from each user and verify they were all received by the leader
    for client in clients:
        message = "test {}".format(client.username)
        client.send_message(message)
        assert leader.expect([message, pexpect.TIMEOUT]) == 0

    logging.info("Finished message tests")

    if debug:
        logging.info("Dropping to an interactive Jabberite prompt {}".format(leader.xmpp_user))
        leader._process.logfile_send = sys.stdout
        leader._process.interact()
