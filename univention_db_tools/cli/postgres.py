import click

from univention_db_tools import Resolution, Host
from .common import postgres_common_options


@click.group(name='pg')
def pg_tools():
	"""PotgreSql related commands"""
	pass


@pg_tools.command(name='backup', help='Backup given database', context_settings=dict(max_content_width=120))
@postgres_common_options
@click.option('-s', '--storage-path', type=click.Path(file_okay=False), help='Path to directory where archives should be stored')
@click.option('-r', '--resolution', type=click.Choice(Resolution), default=Resolution.DAILY.value, show_default=True, help='Backup resolution')
def backup(address: str, port: int, username: str, password: str, db_name: str, db_port: int, db_username: str, db_password: str, storage_path: str, resolution: Resolution):
	from univention_db_tools import DbProvider, PostgresDatabase, create_archiver

	host = Host(address=address, port=port, username=username, password=password)
	db = PostgresDatabase(name=db_name, port=db_port, username=db_username, password=db_password)

	archiver = create_archiver(provider=DbProvider.POSTGRES, host=host)
	archiver.backup(db=db, storage_path=storage_path, resolution=resolution)


@pg_tools.command(name='restore', help='Restore given database')
@postgres_common_options
@click.option('-b', '--backup-path', type=click.Path(exists=True, dir_okay=False), help='Path to archive from which to restore the database')
@click.option('-m', '--match-version', default=True, show_default=True, help='Strict match of dump and major DB version is needed')
def restore(address: str, port: int, username: str, password: str, db_name: str, db_port: int, db_username: str, db_password: str, backup_path: str, match_version: bool):
	from univention_db_tools import DbProvider, PostgresDatabase, create_archiver

	host = Host(address=address, port=port, username=username, password=password)
	db = PostgresDatabase(name=db_name, port=db_port, username=db_username, password=db_password)

	archiver = create_archiver(provider=DbProvider.POSTGRES, host=host)
	archiver.restore(db=db, backup_path=backup_path, match_version=match_version)
