"""
Set of function used to regenerate html files from notebooks.
"""
import fnmatch
import os
import os.path
import shutil


def write_rst_file_with_resources(body, resources):
    """Helper function.
    """
    import nbconvert

    # Create folder if the path not exists
    if not os.path.exists(resources["metadata"]["path"]):
        os.makedirs(resources["metadata"]["path"])

    # Keep resources metadata like image in the rst
    writer = nbconvert.writers.FilesWriter()
    # TODO hack to solve problems with pygment not recognizing ipython2
    body = body.replace(".. code:: ipython2", ".. code:: python")
    body = body.replace(".. code:: ipython3", ".. code:: python")
    writer.write(body, resources, notebook_name=resources["metadata"]["name"])


def write_rst_file_with_filename(body, filename):
    """
    Warning, This write not save image in the transformation to rst format.
    """
    # Create folder if the path not exists
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    # Write rst file
    with open(filename, "w+") as rst_file:
        rst_file.write(body)


def find_notebook_file(root_directory):
    """Get recursively all notebook filenames in the src_directory.

    Args:
        root_directory (str): base directory to search

    Returns:
        (list of str)
    """
    matches = []
    for root, _, filenames in os.walk(root_directory):
        for filename in fnmatch.filter(filenames, '*.ipynb'):

            # Avoid tmp notebook in hidden folder like *-checkpoint.ipynb
            if os.path.basename(root):
                if os.path.basename(root)[0] == '.':
                    continue

            matches.append(os.path.join(root, filename))

    return matches


def action_nbcompile(cfg, **kwds):
    """Compile notebooks into html.
    """
    import nbconvert

    src_directory = cfg["notebook"]['src_directory']
    len_src_directory = len(src_directory)

    nb_filenames = find_notebook_file(src_directory)

    # define documentation rst notebook directory
    dst_rst_directory = os.path.join("doc", "_notebook")

    # remove previous folder
    if os.path.exists(dst_rst_directory):
        shutil.rmtree(dst_rst_directory)

    index_body = """\
========
Notebook
========

.. toctree::
    :glob:
    :caption: Notebook

"""

    rst_exporter = nbconvert.RSTExporter()
    for nb_filename in nb_filenames:
        # Convert each notebook to rst
        body, resources = rst_exporter.from_filename(nb_filename)

        # Remove basename src_directory in the path
        resources["metadata"]["path"] = resources["metadata"]["path"][len_src_directory + 1:]

        # Get the local file_path of the notebook write
        local_file_path = os.path.join(resources["metadata"]["path"], resources["metadata"]["name"])

        # Add dst_rst_directory in the path
        resources["metadata"]["path"] = os.path.join(dst_rst_directory, resources["metadata"]["path"])

        # Write beginning block to download file
        disclaimer = "This file has been generated from the following notebook: :download:`%s`.\n\n" % os.path.basename(nb_filename)
        disclaimer += "Download it if you want to replay it using `jupyter notebook <http://jupyter.org/>`_.\n\n"

        body = disclaimer + body

        # Write rst with his resources
        write_rst_file_with_resources(body, resources)

        # Write notebook file for further download
        shutil.copy(nb_filename, os.path.join(dst_rst_directory, os.path.basename(nb_filename)))

        # Save the notebook rst position in the index body
        index_body += "    " + local_file_path.replace("\\", "/") + "\n"

    # Write rst_index body in the root src directory
    rst_index_filename = os.path.join(dst_rst_directory, "index.rst")
    write_rst_file_with_filename(index_body, rst_index_filename)


def parser_nbcompile(subparsers):
    """Associate a CLI to this tool.

    Notes: The CLI will be a subcommand of pmg.

    Args:
        subparsers (ArgumentParser): entity to create a subparsers

    Returns:
        (string): a unique id for this parser
        (callable): the action to perform
    """
    subparsers.add_parser('nbcompile', help=action_nbcompile.__doc__)

    return 'nbcompile', action_nbcompile
