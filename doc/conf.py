# {# pkglts, sphinx

"""
Configuration for sphinx
see: https://www.sphinx-doc.org/en/master/usage/configuration.html

"""
import os
import re
import sys



# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)
src_dir = os.path.abspath(os.path.join(project_root, "src"))

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, os.path.join(project_root, 'src'))


# -- General configuration ---------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

# try to add more extensions which are not default
# but still useful
# based on the fact that the extension is installed on the system

try:
    import matplotlib.sphinxext.plot_directive
    extensions.append('matplotlib.sphinxext.plot_directive')
except ImportError:
    pass



# default settings that can be redefined outside of the pkglts block
todo_include_todos = True
autosummary_generate = True
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
inheritance_node_attrs = dict(shape='ellipse', fontsize=12,
                              color='orange', style='filled')

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u"pkglts"
copyright = u"2015, pkglts"

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#

# The short X.Y version.
version = "7.1.0"
# The full version, including alpha/beta/rc tags.
release = "7.1.0"


exclude_patterns = ['build', 'dist']

pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
htmlhelp_basename = "pkgltsdoc"


# -- Options for LaTeX output ------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    (u"index", u"pkglts.tex",
     u"pkglts Documentation",
     u"revesansparole",
     u"manual"),
]

# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (u"index", u"pkglts",
     u"pkglts Documentation",
     [u"revesansparole"], 1)
]

# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (u"index", u"pkglts",
     u"pkglts Documentation",
     u"revesansparole",
     u"pkglts",
     u"Building packages with long term support",
     u"Miscellaneous"),
]


# use apidoc to generate developer doc
try:
    from sphinx.ext.apidoc import main
except ImportError:
    from sphinx.apidoc import main


destdir = os.path.abspath(os.path.join(project_root, "doc", "_dvlpt"))

if not os.path.isdir(destdir):
    os.makedirs(destdir)

main(['-e', '-o', destdir, '-d', '4', '-s', source_suffix[1:], '--force', src_dir])

# #}
