from .config import BackupCommandArgs, RestoreCommandArgs, PostgresDbConfig


def postgres_default_backup_command_args() -> BackupCommandArgs:
	postgres_defaults = PostgresDbConfig(name='', username='', password='')
	default_args = BackupCommandArgs(storage_path='', db_config=postgres_defaults)

	return default_args


def postgres_default_restore_command_args() -> RestoreCommandArgs:
	postgres_defaults = PostgresDbConfig(name='', username='', password='')
	default_args = RestoreCommandArgs(backup_path='', db_config=postgres_defaults)

	return default_args
