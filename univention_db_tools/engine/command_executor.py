from contextlib import contextmanager

from fabric import Connection

from .commands import CommandType
from .config import Host


class Executor(object):

	def __init__(self, host: Host):
		self._host = host

	def execute(self, cmd: CommandType, hide: bool = True) -> str:
		with self._connection() as conn:
			res = conn.run(cmd.cmd(), hide=hide)

			return res.stdout.strip()

	def download_file(self, remote_path: str, local_path: str):
		with self._connection() as conn:
			conn.get(remote_path, local_path)

	@contextmanager
	def _connection(self) -> Connection:
		host = self._host
		address = host.address or 'localhost'
		port = host.port
		username = host.username
		password = host.password

		connect_kwargs = {'password': password} if password else {}
		with Connection(host=address, user=username, port=port, connect_kwargs=connect_kwargs) as conn:
			yield conn
