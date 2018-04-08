# {# pkglts, test.pytest_import
import os

import pytest
# #}

# {# pkglts, test.pytest_cmdline_preparse
def pytest_cmdline_preparse(args):
    if 'PYCHARM_HOSTED' not in os.environ:
        args.append("--cov=pkglts")
# #}


# {# pkglts, test.pytest_addoption
def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
                     default=False, help="run slow tests")
# #}


# {# pkglts, test.pytest_collection
def pytest_collection_modifyitems(config, items):
    if not config.getoption("--runslow"):  # skip slow tests
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
# #}
