import pytest
import subprocess
import logging
import yaml
import os

from echochamber.server import XMPPServer
from echochamber.client import Client


def pytest_addoption(parser):
    """Add CLI arguments to pytest"""
    parser.addoption("--show-cli-output", action="store_true",
                     help="show output from all subprocesses (v. noisy)")
    parser.addoption("--debug-mode", action="store_true",
                     help="Enable debug features such as interactive prompts and "
                     "invitation of external jabberite clients.")
    parser.addoption("-C", "--echochamber-config", type=str, default="config.yml",
                     help="Location of the EchoChamber config file.")


@pytest.fixture
def output_trap(request):
    """Trap output by sending to /dev/null if not using debug option"""
    if not pytest.config.getoption("--show-cli-output"):
        return open(os.devnull, "w")


@pytest.fixture
def debug(request):
    """Provide the debug mode status as a fixture"""
    return pytest.config.getoption("--debug-mode")


@pytest.fixture(autouse=True)
def set_loglevel(request):
    if pytest.config.getoption("--verbose"):
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level)


@pytest.fixture(scope="module")
def config(request):
    echochamber_config = request.config.getoption("echochamber_config", None)
    with open(echochamber_config, "r") as config_file:
        return yaml.load(config_file)


@pytest.fixture(scope="module")
def xmpp_server(tmpdir_factory, config):
    """
    Start a local XMPP server for the duration of the test
    """
    tmp_dir = str(tmpdir_factory.mktemp("prosody", numbered=True))
    xmpp_server = XMPPServer(tmp_dir, prosody_bin=config.get("prosody_cmd"))
    xmpp_server.start()

    yield xmpp_server

    # Stop the XMPP server
    xmpp_server.stop()


@pytest.fixture()
def xmpp_account_factory(xmpp_server, output_trap):
    """
    Create an XMPP account on the test XMPP server
    """
    created_accounts = []

    def create_xmpp_account(client_name):
        """Factory for creating XMPP accounts on the server"""
        account_name = "client{name}@{host}".format(name=client_name, host=xmpp_server.host)
        password = "password"

        logging.info("Creating XMPP user %s", account_name)
        add_user_cmd = ["prosodyctl", "--config",  xmpp_server.config_file,
                        "adduser", account_name]
        process = subprocess.Popen(add_user_cmd, stdin=subprocess.PIPE,
                                   stderr=output_trap, stdout=output_trap)
        process.communicate(os.linesep.join([password, password]))
        created_accounts.append(account_name)
        return {"user": account_name, "password": password}

    yield create_xmpp_account

    # Remove accounts that were created with this factory at the end of the test
    for account_name in created_accounts:
        logging.debug("Removing account %s during clean up", account_name)
        del_user_cmd = ["prosodyctl", "--config", xmpp_server.config_file,
                        "deluser", account_name]
        subprocess.check_call(del_user_cmd, stdout=output_trap, stderr=output_trap)


@pytest.fixture()
def client_factory(xmpp_server, xmpp_account_factory, config):
    """
    Create an instance of the Jabberite process connected to the XMPP server
    """
    clients = []

    def create_client(client_name):
        xmpp_account = xmpp_account_factory(client_name)
        client = Client(xmpp_account, port=xmpp_server.c2s_port, config=config)
        clients.append(client)
        return client

    yield create_client

    logging.info("Stopping jabberite clients")
    for client in clients:
        client.stop()
