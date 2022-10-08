from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Union

from pydantic import BaseModel


class Resolution(str, Enum):
	CURRENT = 'current'
	DAILY = 'daily'
	WEEKLY = 'weekly'
	MONTHLY = 'monthly'
	QUARTERLY = 'quarterly'
	YEARLY = 'yearly'


class DbConfig(BaseModel, ABC):
	name: str

	@abstractmethod
	def db_uri(self) -> str:
		raise NotImplementedError


class PostgresDbConfig(DbConfig):
	username: str
	password: str
	host: str = 'localhost'
	port: int = 5432

	def db_uri(self) -> str:
		return f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}'


class BackupCommandArgs(BaseModel):

	storage_path: Union[str, Path]
	db_config: Union[PostgresDbConfig]
	resolution: Resolution = Resolution.DAILY
	force: bool = False


class RestoreCommandArgs(BaseModel):

	backup_path: Union[str, Path]
	db_config: Union[PostgresDbConfig]
