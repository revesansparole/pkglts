import os
import os.path
import fnmatch
import nbconvert
import shutil


def write_rst_file_with_resources(body, resources):
    # Create folder if the path not exists
    if not os.path.exists(resources["metadata"]["path"]):
        os.makedirs(resources["metadata"]["path"])

    # Keep resources metadata like image in the rst
    writer = nbconvert.writers.FilesWriter()
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
    # Get recursively all notebook filenames in the src_directory
    matches = []
    for root, dirnames, filenames in os.walk(root_directory):
        for filename in fnmatch.filter(filenames, '*.ipynb'):

            # Avoid tmp notebook in hidden folder like *-checkpoint.ipynb
            if len(os.path.basename(root)) > 0:
                if os.path.basename(root)[0] == '.':
                    continue

            matches.append(os.path.join(root, filename))

    return matches


def main(cfg, target=".", overwrite=False):
    """Main function called to walk the package

    Args:
        cfg (Config):  current package configuration
        target (str): place to write plugin def into
        overwrite (bool): whether or not to overwrite previous definition
                          files. Default to False.
    """
    del target
    del overwrite

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
        resources["metadata"]["path"] = \
            resources["metadata"]["path"][len_src_directory + 1:]

        # Get the local file_path of the notebook write
        local_file_path = os.path.join(resources["metadata"]["path"],
                                       resources["metadata"]["name"])

        # Add dst_rst_directory in the path
        resources["metadata"]["path"] = os.path.join(
            dst_rst_directory, resources["metadata"]["path"])

        # Write rst with this resources
        write_rst_file_with_resources(body, resources)

        # Save the notebook rst position in the index body
        index_body += "    " + local_file_path.replace("\\", "/") + "\n"

    # Write rst_index body in the root src directory
    rst_index_filename = os.path.join(dst_rst_directory, "index.rst")
    write_rst_file_with_filename(index_body, rst_index_filename)
