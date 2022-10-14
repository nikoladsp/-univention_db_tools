.. sectnum::

Packaging
=========

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
  * `sphinx <https://www.sphinx-doc.org/en/master/>`_ 4.5.0 - documentation generator
  * `univention_sphinx_book_theme <https://git.knut.univention.de/univention/documentation/univention_sphinx_book_theme>`_ 0.0.8
  * `univention_sphinx_extension <https://git.knut.univention.de/univention/documentation/univention_sphinx_extension>`_ 0.0.12


Package version
-----------------------------------

In order to get version programmatically from ``debian/changelog`` file, we use :func:`setup.get_version` function.

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

Building documentation
-----------------------------------

To build documentation in your (virtual) environment:

.. code-block:: bash

   python setup.py build_sphinx
