# {# pkglts, sphinx

"""
Configuration for sphinx
see: https://www.sphinx-doc.org/en/master/usage/configuration.html

"""

{%- if 'pyproject' is available %}
import os
{%- endif %}
import sys
{%- if sphinx.gallery != "" %}
import warnings
{%- endif %}

{% if 'pyproject' is available %}

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)
src_dir = os.path.abspath(os.path.join(project_root, "src"))

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, os.path.join(project_root, 'src'))
{% endif %}

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
{%- if sphinx.gallery != "" %}
    'sphinx_gallery.gen_gallery',
{%- endif %}
]

# try to add more extensions which are not default
# but still useful
# based on the fact that the extension is installed on the system

try:
    import matplotlib.sphinxext.plot_directive
    extensions.append('matplotlib.sphinxext.plot_directive')
except ImportError:
    pass

{% if sphinx.gallery != "" -%}
sphinx_gallery_conf = {
    'examples_dirs': "../{{ sphinx.gallery }}",   # path to your example scripts
    'gallery_dirs': "_gallery",  # path where to save gallery generated examples
    'filename_pattern': "plot_",
    'ignore_pattern': "^(?!plot_)",
    'download_all_examples': False,
    'within_subsection_order': "ExampleTitleSortKey",
}
{%- endif %}

# default settings that can be redefined outside of the pkglts block
todo_include_todos = True
autosummary_generate = True
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
inheritance_node_attrs = dict(shape='ellipse', fontsize=12,
                              color='orange', style='filled')

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = {
    '.rst': 'restructuredtext',
}

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = "{{ base.pkg_full_name }}"
copyright = "{{ license.year }}, {{ base.pkg_full_name }}"

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
{% if 'version' is available %}
# The short X.Y version.
version = "{{ version.major }}.{{ version.minor }}.{{ version.post }}"
# The full version, including alpha/beta/rc tags.
release = "{{ version.major }}.{{ version.minor }}.{{ version.post }}"
{% endif %}

exclude_patterns = ['build', 'dist']

pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------

html_theme = "{{ sphinx.theme }}"
html_static_path = ['_static']
htmlhelp_basename = "{{ base.pkgname }}doc"


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
    ("index", "{{ base.pkgname }}.tex",
     "{{ base.pkgname|replace('_', '\_') }} Documentation",
     "{{ base.authors[0][0]|replace('_', '\_') }}",
     {% if 'pyproject' is available %}"manual"{% else %}"article"{% endif %}),
]

# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ("index", "{{ base.pkgname }}",
     "{{ base.pkgname }} Documentation",
     ["{{ base.authors[0][0] }}"], 1)
]

# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ("index", "{{ base.pkgname }}",
     "{{ base.pkgname }} Documentation",
     "{{ base.authors[0][0] }}",
     "{{ base.pkgname }}",
     "{{ doc.description }}",
     "Miscellaneous"),
]

{% if 'pyproject' is available and sphinx.autodoc_dvlpt %}
# use apidoc to generate developer doc
try:
    from sphinx.ext.apidoc import main
except ImportError:
    from sphinx.apidoc import main


destdir = os.path.abspath(os.path.join(project_root, "doc", "_dvlpt"))

if not os.path.isdir(destdir):
    os.makedirs(destdir)

main(['-e', '-o', destdir, '-d', '4', '--force', src_dir])
{% endif %}

{%- if sphinx.gallery != "" %}
# Remove matplotlib agg warnings from generated doc when using plt.show
warnings.filterwarnings("ignore", category=UserWarning,
                        message='Matplotlib is currently using agg, which is a'
                                ' non-GUI backend, so cannot show the figure.')
{% endif %}
# #}
