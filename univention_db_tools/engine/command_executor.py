import socket
from contextlib import contextmanager
from os import getlogin
from typing import Union, List

import invoke
from fabric import Connection

from .commands import CommandType
from .config import Host


class Executor(object):

	def __init__(self, host: Host):
		self._host = host

	def execute(self, cmd: Union[CommandType, List[CommandType]], hide: bool = True, raise_on_error: bool = True) -> str:
		res = invoke.Result()

		if not isinstance(cmd, list):
			cmd = [cmd]

		with self._connection() as conn:
			for c in cmd:
				try:
					res = conn.run(c.cmd(), hide=hide)
				except invoke.exceptions.UnexpectedExit as e:
					if raise_on_error:
						raise RuntimeError(e)
		return res.stdout.strip()

	def download_file(self, remote_path: str, local_path: str):
		if self._local_connection():
			invoke.run(f'cp {remote_path} {local_path}')
		else:
			with self._connection() as conn:
				conn.get(remote_path, local_path)

	@contextmanager
	def _connection(self) -> Connection:
		host = self._host
		address = host.address or 'localhost'
		port = host.port
		username = host.username
		password = host.password

		if self._local_connection():
			def _invoke_wrapper():
				return invoke

			yield _invoke_wrapper()
		else:
			connect_kwargs = {'password': password} if password else {}
			with Connection(host=address, user=username, port=port, connect_kwargs=connect_kwargs) as conn:
				yield conn

	def _local_connection(self) -> bool:
		host = self._host
		address = host.address or 'localhost'
		port = host.port
		username = host.username

		return 22 == port and socket.getfqdn(address) in ['localhost', '0.0.0.0'] and username in [getlogin(), 'root']
