import click

from univention_db_tools import postgres_default_backup_command_args

dflt_cmd_cfg = postgres_default_backup_command_args()
dflt_db_cfg = dflt_cmd_cfg.db_config


def postgres_common_command_options(function):

    # options and arguments are evaluated in reverse order!
    function = click.option('-P', '--password', default=dflt_db_cfg.password, show_default=True, help='Database account password')(function)
    function = click.option('-U', '--username', default=dflt_db_cfg.username, show_default=True, help='Database account username')(function)
    function = click.option('-p', '--port', default=dflt_db_cfg.port, show_default=True, help='Database port')(function)
    function = click.option('-h', '--host', default=dflt_db_cfg.host, show_default=True, help='Database host')(function)
    function = click.option('-n', '--name', default=dflt_db_cfg.name, show_default=True, help='Database name')(function)

    return function
