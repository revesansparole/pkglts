"""List data in current directory and sub package
"""

from pathlib import Path

loc_dir = Path(__file__).parent


def list_data():
    """Iterate on all files in the package
    that are not python files.
    """
    for pth in loc_dir.glob("**/*.*"):
        if pth.suffix not in (".py", ".pyc", ".pyo"):
            yield pth.relative_to(loc_dir)
