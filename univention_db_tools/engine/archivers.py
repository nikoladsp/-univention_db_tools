from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Union

from .config import Resolution, DbProvider, Host, BackupArgs, RestoreArgs
from .command_executor import Executor
from .commands import PostgresVersionCommand, PostgresBackupCommand


class Archiver(ABC):

	def __init__(self, host: Host):
		self._host = host

	@abstractmethod
	def backup(self, args: BackupArgs):
		raise NotImplementedError

	@abstractmethod
	def restore(self, args: RestoreArgs):
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

	def backup(self, args: BackupArgs):
		self._create_storage_layout(args.storage_path)

		db = args.db
		executor = Executor(self._host)

		backup_path = self._backup_path(executor=executor, args=args)
		cmd = PostgresBackupCommand(db=db, backup_path=backup_path)
		executor.execute(cmd=cmd)

	def restore(self, args: RestoreArgs):
		pass

	def _backup_path(self, executor: Executor, args: BackupArgs) -> str:
		db = args.db
		provider = DbProvider.POSTGRES

		cmd = PostgresVersionCommand(db=db)
		full_version = executor.execute(cmd=cmd)

		version = self._major_db_version(full_version)
		backup_name = self._backup_name(name=db.name, provider=provider, version=version, resolution=args.resolution)

		return f'/tmp/{backup_name}'
