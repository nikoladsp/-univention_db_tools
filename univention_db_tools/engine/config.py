from abc import ABC, abstractmethod
from enum import Enum
from os import getlogin
from typing import Union, List, Set, Optional, TypeVar

from pydantic import BaseModel

DatabaseType = TypeVar('DatabaseType', bound='Database')


class Resolution(str, Enum):
	CURRENT = 'current'
	DAILY = 'daily'
	WEEKLY = 'weekly'
	MONTHLY = 'monthly'
	QUARTERLY = 'quarterly'
	YEARLY = 'yearly'


class DbProvider(str, Enum):
	POSTGRES = 'pg'


class SupportedDb(BaseModel):
	provider: DbProvider = DbProvider.POSTGRES
	versions: Set[Union[str, int]]


def supported_dbs() -> List[SupportedDb]:
	return [
		SupportedDb(provider=DbProvider.POSTGRES, versions=[10, 11, 12, 13, 14]),
	]


def db_supported(name: str, version: Union[int, str], db_list: List[SupportedDb] = None) -> bool:
	for db in db_list or supported_dbs():
		prov = db.provider
		if name.lower() in [prov.name.lower(), prov.value.lower()] and str(version) in set(map(str, db.versions)):
			return True

	return False


class Host(BaseModel):
	username: str = getlogin()
	password: Optional[str] = None
	address: str = 'localhost'
	port: int = 22


class Database(BaseModel, ABC):
	name: str

	@abstractmethod
	def db_uri(self) -> str:
		raise NotImplementedError


class PostgresDatabase(Database):
	username: str
	password: str
	host: str = 'localhost'
	port: int = 5432

	def db_uri(self) -> str:
		return f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}'
