# -- Path setup --------------------------------------------------------------
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath('../univention_db_tools'))
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'univention-db-tools'
copyright = '{}, Univention GmbH'.format(date.today().year)
author = 'Univention GmbH'

# -- General configuration ---------------------------------------------------
extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.intersphinx',
	'sphinx.ext.todo',
	'sphinx.ext.viewcode',
	'sphinx.ext.autosummary',
	'sphinx.ext.inheritance_diagram',
	'sphinx.ext.graphviz',
	'univention_sphinx_extension',
	'sphinxcontrib.spelling',
]

templates_path = ['templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {
	'python': ('https://docs.python.org/3.7', None),  # noqa: WPS323
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['static']
html_title = project
