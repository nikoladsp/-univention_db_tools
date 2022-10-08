import click

from univention_db_tools import Resolution, PostgresDbConfig, BackupCommandArgs, RestoreCommandArgs
from .common import dflt_cmd_cfg, postgres_common_command_options


@click.group(name='pg')
def pg_tools():
	"""PotgreSql related commands"""
	pass


@pg_tools.command(name='backup', help='Backup given database', context_settings=dict(max_content_width=120))
@postgres_common_command_options
@click.option('-s', '--storage-path', type=click.Path(), default=dflt_cmd_cfg.storage_path, show_default=True, help='Path to directory where archives should be stored')
@click.option('-r', '--resolution', type=click.Choice(Resolution), default=Resolution.DAILY.value, show_default=True, help='Backup resolution')
@click.option('-f', '--force', is_flag=True, default=dflt_cmd_cfg.force, show_default=True, help='Overwrite archive if exists')
def backup(name: str, host: str, port: int, username: str, password: str, storage_path: str, resolution: Resolution, force: bool):
	db_config = PostgresDbConfig(name=name, host=host, port=port, username=username, password=password)
	command_args = BackupCommandArgs(storage_path=storage_path, db_config=db_config, resolution=resolution, force=force)

	print('backup')
	print(command_args)


@pg_tools.command(name='restore', help='Restore given database')
@postgres_common_command_options
@click.option('-b', '--backup-path', type=click.Path(exists=True), default=dflt_cmd_cfg.storage_path, show_default=True, help='Path to archive from which to restore the database')
def restore(name: str, host: str, port: int, username: str, password: str, backup_path: str):
	db_config = PostgresDbConfig(name=name, host=host, port=port, username=username, password=password)
	command_args = RestoreCommandArgs(backup_path=backup_path, db_config=db_config)

	print('restore')
	print(command_args)
