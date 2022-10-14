import click

from univention_db_tools import Resolution, Host
from .common import postgres_common_command_options


@click.group(name='pg')
def pg_tools():
	"""PotgreSql related commands"""
	pass


@pg_tools.command(name='backup', help='Backup given database', context_settings=dict(max_content_width=120))
@postgres_common_command_options
@click.option('-s', '--storage-path', type=click.Path(), help='Path to directory where archives should be stored')
@click.option('-r', '--resolution', type=click.Choice(Resolution), default=Resolution.DAILY, show_default=True, help='Backup resolution')
@click.option('-f', '--force', is_flag=True, default=False, show_default=True, help='Overwrite archive if exists')
def backup(address: str, port: int, username: str, password: str, name: str, db_port: int, db_username: str, db_password: str, storage_path: str, resolution: Resolution, force: bool):
	from univention_db_tools import PostgresDatabase, PostgresArchiver, BackupArgs

	host = Host(address=address, port=port, username=username, password=password)
	db = PostgresDatabase(name=name, port=db_port, username=db_username, password=db_password)
	args = BackupArgs(db=db, storage_path=storage_path,resolution=resolution, force=force)

	archiver = PostgresArchiver(host=host)
	archiver.backup(args=args)


@pg_tools.command(name='restore', help='Restore given database')
@postgres_common_command_options
@click.option('-b', '--backup-path', type=click.Path(exists=True), help='Path to archive from which to restore the database')
def restore(address: str, port: int, username: str, password: str, name: str, db_port: int,db_username: str, db_password: str, backup_path: str):
	from univention_db_tools import PostgresDatabase, PostgresArchiver, RestoreArgs

	host = Host(address=address, port=port, username=username, password=password)
	db = PostgresDatabase(name=name, port=db_port, username=db_username, password=db_password)
	args = RestoreArgs(db=db, backup_path=backup_path)

	archiver = PostgresArchiver(host=host)
	archiver.restore(args=args)
