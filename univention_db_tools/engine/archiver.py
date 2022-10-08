from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from .config import Resolution, BackupCommandArgs, RestoreCommandArgs


class Archiver(ABC):

	@abstractmethod
	def backup(self, args: BackupCommandArgs):
		raise NotImplementedError

	@abstractmethod
	def restore(self, args: RestoreCommandArgs):
		raise NotImplementedError

	@classmethod
	def _create_storage_layout(cls, path: Union[str, Path]):
		storage_path = Path(path)
		storage_path.mkdir(parents=True, exist_ok=True)
		for res in Resolution:
			p = storage_path.joinpath(res.value)
			p.mkdir(exist_ok=True)
