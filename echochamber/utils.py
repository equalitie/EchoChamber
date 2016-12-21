import time
import logging
import socket


def find_available_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def create_client_connections(client_factory, num_clients, room_name="test", proxy_port=None):
    """
    Helper to create N jabberite client connections to an XMPP room.

    Returns a list of contected clients
    """
    clients = []
    for client_id in range(0, num_clients):
        client = client_factory(client_id, port=proxy_port)
        client.connect("messaging-test")  # Connect to the XMPP room
        clients.append(client)

    time.sleep(1)  # Wait for all users to finish joining the room
    return clients


def establish_channel(clients):
    """
    Help function which establishes a conversation with a list of connected Clients

    The first client is selected as the channel leader
    """
    leader, clients = clients[0], clients[1:]
    conversation_id = leader.create_conversation()
    leader.select_conversation(conversation_id)
    logging.debug("Created and selected conversation %d", conversation_id)

    # Invite all the other users and get each of them to join the conversation.
    for client in clients:
        leader.invite_and_join_conversation(client)

    return conversation_id
