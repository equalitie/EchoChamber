import os
import logging
import socket
import subprocess

import jinja2


def find_available_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


class XMPPServer(object):
    """The helper class used to manage the XMPP server"""
    def __init__(self, tmpdir, host="localhost", prosody_bin="/usr/bin/prosody"):
        self.tmpdir = str(tmpdir)
        self.host = host
        self.prosody_bin = prosody_bin
        self._process = None

        self.config_file = None
        # Pick a random available port for s2s and c2s connections.
        # self.s2s_port = find_available_port()
        # self.c2s_port = find_available_port()

        # Use the default s2s and c2s ports for ease when testing locally.
        self.s2s_port = 5269
        self.c2s_port = 5222

        if not os.path.isfile(self.prosody_bin):
            raise ValueError("Prosody binary not found at %s", self.prosody_bin)

    def create_config(self):
        """Create a Prosody config file from a template"""
        config_data = {
            "host": self.host,
            "s2s_port": self.s2s_port,
            "c2s_port": self.c2s_port,
        }
        paths = {
            "data_path": os.path.join(self.tmpdir, "var", "lib", "prosody"),
            "run_path": os.path.join(self.tmpdir, "var", "run", "prosody"),
            "sock_path": os.path.join(self.tmpdir, "var", "run", "echochamber"),
            "config_path": os.path.join(self.tmpdir, "etc", "prosody"),
            "certs_path": os.path.join(self.tmpdir, "etc", "prosody", "certs"),
            "log_path": os.path.join(self.tmpdir, "var", "log"),
        }
        for path in paths.values():
            os.makedirs(path)
        config_data.update(paths)

        # Substitute config file template with the correct paths
        with open(os.path.join("templates", "prosody.cfg.lua"), "r") as template_file:
            config_template = jinja2.Template(template_file.read())
        rendered_config = config_template.render(config_data)

        # Write out configuration file with correct temporary paths
        config_filename = os.path.join(paths["config_path"], "prosody.cfg.lua")
        with open(config_filename, "w") as config_file:
            config_file.write(rendered_config)

        return config_filename

    def start(self):
        """Start the XMPP server as a separate process."""
        self.config_file = self.create_config()
        prosody_cmd = ["--config", self.config_file]
        logging.info("Starting prosody with config: %s", self.config_file)

        self._process = subprocess.Popen([self.prosody_bin] + prosody_cmd, shell=False,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         stdin=subprocess.PIPE,
                                         )

        # import sys
        # self._process = pexpect.spawn(self.prosody_bin, prosody_cmd, timeout=None,
        #                               logfile=sys.stdout)
        # # Wait for server to start
        # self._process.expect("Activated service 'c2s'")

        # # Raise exception if Prosody could not bind to port
        # if "Failed to open server" in self._process.before:
        #     raise Exception("Prosody could not start. Please kill any other "
        #                     "Prosody instances which are running.")

    def stop(self):
        """Stop application process."""
        if self._process:
            logging.info("Stopping prosody")
            self._process.kill()

    def __repr__(self):
        return "<XMPPServer from {}>".format(self.config_file)
