from pathlib import Path

import pytest
from pkglts.option.reqs.find_requirements import find_reqs, action_find_reqs
from pkglts.small_tools import ensure_created, rmdir
from pkglts.config_management import Config


@pytest.fixture()
def tmp_dir():
    pth = Path("tagadareqs")

    ensure_created(pth)

    yield pth

    rmdir(pth)


def test_find_reqs_parses_files(tmp_dir):
    pth = tmp_dir / "toto.py"
    with open(pth, "w") as fhw:
        fhw.write(
            "import os\n"
            "from sys import argv\n"
            "\n"
            "import pytest\n"
            "import numpy as np\n"
            "from pandas import DataFrame\n"
            "from toto import failure\n"
            "\n"
            "a = 1\n"
            "\n"
            "from doom import pestilence\n"
            ""
        )

    reqs = find_reqs(pth)

    for name in ("os", "sys", "pytest", "numpy", "pandas", "toto", "doom"):
        assert name in reqs


def test_myoutput(tmp_dir, capsys):
    pth = tmp_dir / "toto.py"
    with open(pth, "w") as fhw:
        fhw.write(
            "import os\n"
            "from sys import argv\n"
            "\n"
            "import pytest\n"
            "import numpy as np\n"
            "from pandas import DataFrame\n"
            "from toto import failure\n"
            "\n"
            "a = 1\n"
            "\n"
            "from doom import pestilence\n"
            ""
        )

    cfg = Config(dict(base={"pkgname": "walou", "namespace": None, "owner": "moi", "url": None}))
    action_find_reqs(cfg)

    out, err = capsys.readouterr()
    assert "standard" in out
