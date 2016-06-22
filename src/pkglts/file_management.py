
def write_file(pth, content):
    """Write the content of a file on a local path and
    register associated hash for further modification
    tests.

    Args:
        pth (str): path to the new created file
        content (str): content to write on disk

    Returns:

    """
    with open(pth, 'wb') as f:
        f.write(content.encode("utf-8"))
