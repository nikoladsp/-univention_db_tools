import click

from univention_db_tools import Resolution
from .common import dflt_cmd_cfg, postgres_common_command_options


@click.group(name='pg')
def pg_tools():
	"""PotgreSql related commands"""
	pass


@pg_tools.command(name='backup', help='Backup given database', context_settings=dict(max_content_width=120))
@postgres_common_command_options
@click.option('-s', '--storage-path', type=click.Path(), default=dflt_cmd_cfg.storage_path, show_default=True, help='Path to directory where archives should be stored')
@click.option('-r', '--resolution', type=click.Choice(Resolution), default=dflt_cmd_cfg.resolution, show_default=True, help='Backup resolution')
@click.option('-f', '--force', is_flag=True, default=dflt_cmd_cfg.force, show_default=True, help='Overwrite archive if exists')
def backup(name: str, host: str, port: int, username: str, password: str, storage_path: str, resolution: Resolution, force: bool):
	from univention_db_tools import PostgresDbConfig, BackupCommandArgs, PostgresArchiver

	db_config = PostgresDbConfig(name=name, host=host, port=port, username=username, password=password)
	args = BackupCommandArgs(storage_path=storage_path, db_config=db_config, resolution=resolution, force=force)

	archiver = PostgresArchiver()
	archiver.backup(args)


@pg_tools.command(name='restore', help='Restore given database')
@postgres_common_command_options
@click.option('-b', '--backup-path', type=click.Path(exists=True), default=dflt_cmd_cfg.storage_path, show_default=True, help='Path to archive from which to restore the database')
def restore(name: str, host: str, port: int, username: str, password: str, backup_path: str):
	from univention_db_tools import PostgresDbConfig, RestoreCommandArgs, PostgresArchiver

	db_config = PostgresDbConfig(name=name, host=host, port=port, username=username, password=password)
	args = RestoreCommandArgs(backup_path=backup_path, db_config=db_config)

	archiver = PostgresArchiver()
	archiver.backup(args)
