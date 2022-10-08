import subprocess
import sys

import setuptools


def get_version() -> str:
	from os.path import dirname, join
	import pkg_resources

	pkg_name = 'python-debian'
	installed = {pkg.key for pkg in pkg_resources.working_set}
	pkg_missing = pkg_name not in installed

	if pkg_missing:
		subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg_name])

	globals()['debian'] = __import__('debian')
	from debian.changelog import Changelog

	try:
		changelog_path = join(dirname(__file__), 'debian/changelog')
		with open(changelog_path, 'r') as fd:
			changelog = Changelog(fd)
			version = changelog.version
	except FileNotFoundError:
		version = '0.0.0'

	if pkg_missing:
		subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-y', pkg_name])

	return version


if __name__ == '__main__':
	setuptools.setup(version=get_version())
