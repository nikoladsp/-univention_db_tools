from datetime import datetime, timezone
from tempfile import TemporaryDirectory

from .archiver import Archiver
from .config import BackupCommandArgs, RestoreCommandArgs


class PostgresArchiver(Archiver):

	def backup(self, args: BackupCommandArgs):
		self._create_storage_layout(args.storage_path)

		with TemporaryDirectory() as dirname:
			db_config = args.db_config
			dump_file_path = f'{dirname}/{db_config.name}_{datetime.now(timezone.utc).strftime("%Y_%m_%d")}.dump'
			cmd = f'pg_dump -d {db_config.name} -h {db_config.host} -p {db_config.port} -U {db_config.username} -W {db_config.password} --format=custom --if-exists --clean --no-owner --no-acl -f {dump_file_path}'
			print(cmd)

	def restore(self, args: RestoreCommandArgs):
		pass
