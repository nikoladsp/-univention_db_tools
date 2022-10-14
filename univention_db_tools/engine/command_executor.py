import socket
from os import getlogin

from fabric import Connection
from invoke import run

from .commands import CommandType
from .config import Host


class Executor(object):

	def __init__(self, host: Host):
		self._host = host

	def execute(self, cmd: CommandType) -> str:
		host_config = self._host
		address = host_config.address
		port = host_config.port
		username = host_config.username
		password = host_config.password

		if address and socket.getfqdn(address) in ['localhost', '0.0.0.0'] and username == getlogin():
			res = run(cmd.cmd())
		else:
			connect_kwargs = {'password': password} if password else {}
			with Connection(host=address, user=username, port=port, connect_kwargs=connect_kwargs) as conn:
				res = conn.run(cmd.cmd())

		return res.stdout.strip()
