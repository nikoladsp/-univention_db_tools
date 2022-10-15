from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Union

from .command_executor import Executor
from .commands import PostgresVersionCommand, PostgresBackupCommand
from .config import Resolution, DbProvider, DatabaseType, Host


def create_archiver(provider: DbProvider, host: Host):
	providers = {
		DbProvider.POSTGRES: PostgresArchiver,
	}

	provider = providers.get(provider, None)

	if not provider:
		raise RuntimeError(f'Unsupported provider: {provider}')

	return provider(executor=Executor(host))


class Archiver(ABC):

	def __init__(self, executor: Executor):
		self._executor = executor

	@abstractmethod
	def backup(self, db: DatabaseType, storage_path: str, resolution: Resolution = Resolution.DAILY):
		raise NotImplementedError

	@abstractmethod
	def restore(self, db: DatabaseType, backup_path: str):
		raise NotImplementedError

	@classmethod
	def _backup_name(cls, name: str, provider: DbProvider, version: str, resolution: Resolution) -> str:
		timestamp = datetime.utcnow()
		timestamp_format = '%Y%m%d_%H%M%S' if resolution == Resolution.CURRENT else '%Y%m%d'

		return f'{name}_{provider.value}_{version}_{timestamp.strftime(timestamp_format)}.dump'

	@classmethod
	def _create_storage_layout(cls, path: Union[str, Path]):
		storage_path = Path(path)
		storage_path.mkdir(parents=True, exist_ok=True)

		res: Resolution
		for res in Resolution:
			p = storage_path.joinpath(res.value)
			p.mkdir(exist_ok=True)

	@classmethod
	def _major_db_version(cls, version: str) -> str:
		pos = version.find('.')
		if -1 != pos:
			return version[:pos]
		else:
			return version


class PostgresArchiver(Archiver):

	def backup(self, db: DatabaseType, storage_path: str, resolution: Resolution = Resolution.DAILY):
		self._create_storage_layout(storage_path)

		backup_path = self._backup_path(db=db, resolution=resolution)
		cmd = PostgresBackupCommand(db=db, backup_path=backup_path)
		self._executor.execute(cmd=cmd)

	def restore(self, db: DatabaseType, backup_path: str):
		pass

	def _backup_path(self, db: DatabaseType, resolution: Resolution) -> str:
		provider = DbProvider.POSTGRES

		cmd = PostgresVersionCommand(db=db)
		full_version = self._executor.execute(cmd=cmd)

		version = self._major_db_version(full_version)
		backup_name = self._backup_name(name=db.name, provider=provider, version=version, resolution=resolution)

		return f'/tmp/{backup_name}'
