import click

from univention_db_tools import Host

default_host = Host()


def postgres_common_command_options(function):

    # options and arguments are evaluated in reverse order!
    function = click.option('-P', '--db-password', help='Database account password')(function)
    function = click.option('-U', '--db-username', help='Database account username')(function)
    function = click.option('-t', '--db-port', default=5432, show_default=True, help='Database service port')(function)
    function = click.option('-n', '--name', help='Database name')(function)
    function = click.option('-p', '--password', default=default_host.password, show_default=True, help='Database host address password')(function)
    function = click.option('-u', '--username', default=default_host.username, show_default=True, help='Database host address username')(function)
    function = click.option('-o', '--port', default=default_host.port, show_default=True, help='Database host address port')(function)
    function = click.option('-a', '--address', default=default_host.address, show_default=True, help='Database host address')(function)

    return function
