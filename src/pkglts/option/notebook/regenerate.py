import os
import os.path
import fnmatch
import nbconvert
import shutil


def write_rst_file(filename, body):
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


def main(env, target=".", overwrite=False):
    """Main function called to walk the package

    Args:
        env: (dict of (str, dict)) package configuration parameters
        target (str): place to write plugin def into
        overwrite (bool): whether or not to overwrite previous definition
                          files. Default to False.
    """
    del target
    del overwrite

    src_directory = env.globals["notebook"].src_directory
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

        output_rst_file_name = os.path.join(
            resources["metadata"]["path"],
            resources["metadata"]["name"] + resources["output_extension"])

        # Remove basename src_directory in the path
        output_rst_file_name = output_rst_file_name[len_src_directory + 1:]

        # Add dst_rst_directory in the path
        rst_filename = os.path.join(dst_rst_directory, output_rst_file_name)

        write_rst_file(rst_filename, body)

        # Update rst_index body
        index_body += "    " + output_rst_file_name.replace("\\", "/") + "\n"

    # Write rst_index body in the root src directory
    rst_index_filename = os.path.join(dst_rst_directory, "index.rst")
    write_rst_file(rst_index_filename, index_body)
