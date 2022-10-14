from abc import ABC, abstractmethod
from typing import TypeVar

from .config import DatabaseType, PostgresDatabase

CommandType = TypeVar('CommandType', bound='Command')


class Command(ABC):

	def __init__(self, db: DatabaseType):
		self._db = db

	@abstractmethod
	def cmd(self) -> str:
		raise NotImplementedError


class PostgresCommand(Command, ABC):

	def _finalize_cmd(self, command: str) -> str:
		db: PostgresDatabase = self._db
		if db.password:
			command = f'PGPASSWORD="{db.password}" {command}'

		return command


class PostgresVersionCommand(PostgresCommand):

	def cmd(self) -> str:
		db: PostgresDatabase = self._db
		command = f'psql -qAtX -h {db.host} -p {db.port} -U {db.username} -d {db.name} -c \'SHOW server_version;\''

		return self._finalize_cmd(command)


class PostgresBackupCommand(PostgresCommand):

	def __init__(self, db: DatabaseType, backup_path: str):
		super().__init__(db)
		self._backup_path = backup_path

	def cmd(self) -> str:
		db: PostgresDatabase = self._db
		command = f'pg_dump -d {db.name} -h {db.host} -p {db.port} -U {db.username} --format=custom --if-exists --clean --no-owner --no-acl -f {self._backup_path}'

		return self._finalize_cmd(command)
