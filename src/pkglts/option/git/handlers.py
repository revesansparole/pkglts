"""
Set of function to extend jinja2 environment.
"""
import logging
import re
import subprocess

from unidecode import unidecode

LOGGER = logging.getLogger(__name__)


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    del cfg

    try:
        log = subprocess.check_output(['git', 'log', '--all', '--use-mailmap']).decode('utf-8')
        commiters = re.findall(r'Author: (.* <.*@.*>)\n', unidecode(log))
        ccs = [(commiters.count(name), name) for name in set(commiters)]
        contributors = [name for nb, name in sorted(ccs, reverse=True)]
    except KeyError:
        LOGGER.warning("Please add git to your $PATH")
        contributors = ["I failed to construct the contributor list"]
    except subprocess.CalledProcessError as err:
        contributors = ["Pb with git, %s" % str(err)]

    return {'contributors': contributors}
