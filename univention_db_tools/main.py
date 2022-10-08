#!/usr/bin/env python

import click
# from backend_2m.cli.commands import db_tools
# from backend_2m.settings import get_settings

@click.group()
def manage():
	pass


def main():
	# manage.add_command(db_tools)

	manage()
	print('ende')


	# settings = get_settings()
	# print(settings)


if __name__ == '__main__':
	main()
