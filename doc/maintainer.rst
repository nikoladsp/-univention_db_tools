Maintainer's guide
==================

Prerequisites
-----------------------------------

It is possible to build and install `univention-db-tools` using both setuptools and Debian package.

Main dependencies are:

  * `click <https://palletsprojects.com/p/click/>`_ - package for creating command line interfaces
  * `pydantic <https://pydantic-docs.helpmanual.io/>`_ - data validation and settings management using Python type annotations.

Dependencies for running tests:

  * `pytest <https://docs.pytest.org/en/latest/>`_ - testing framework
  * `tox <https://tox.wiki/en/latest/>`_ - generic virtualenv management and test command line tool

Dependencies for building documentation:

  * `graphviz <https://graphviz.org/>`_ - graph visualization software
  * `sphinx <https://www.sphinx-doc.org/en/master/>`_ - documentation generator

Building PyPI package
-----------------------------------

To build and install in your virtual environment:

.. code-block:: bash

   python3.7 -m venv venv
   source venv/bin/activate
   python setup.py install

If you want (or need) to use wheel package:

.. code-block:: bash

   python3.7 -m venv venv
   source venv/bin/activate
   pip install wheel
   python setup.py bdist_wheel

Resulting wheel file will be located in ``./dist`` folder. After this step you can install it or distribute it.

Building DEB package
-----------------------------------

To build Debian package:

.. code-block:: bash

   apt-get build-dep .
   dpkg-buildpackage -b -uc -us

Package version
-----------------------------------

In order to get version programmatically from ``debian/changelog`` file, we use this function in ``setup.py``:

.. code-block:: python

   def get_version() -> str:
       import re
       from os.path import dirname, join

       topline = re.compile(
           r'^(\w%(name_chars)s*) \(([^\(\) \t]+)\)'
           r'((\s+%(name_chars)s+)+)\;'
           % {'name_chars': '[-+0-9a-z.]'},
           re.IGNORECASE)

       version = '0.0.0'

       try:
           changelog_path = join(dirname(__file__), 'debian/changelog')
           with open(changelog_path, 'r') as fd:
               for line in fd.readlines():
                   top_match = topline.match(line.strip())
                   if top_match:
                       version = top_match.group(2)
                       break
       except FileNotFoundError:
           pass

       return version
