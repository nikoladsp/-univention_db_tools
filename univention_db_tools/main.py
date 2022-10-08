#!/usr/bin/env python

import click

from univention_db_tools.commands import pg_tools


@click.group()
def manage():
	pass


def main():
	manage.add_command(pg_tools)

	manage()


if __name__ == '__main__':
	main()
