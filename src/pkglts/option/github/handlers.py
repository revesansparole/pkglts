import logging
import re
import subprocess

logger = logging.getLogger(__name__)


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    del cfg
    
    try:
        log = subprocess.check_output(['git', 'log', '--all']).decode('utf-8')
    except KeyError:
        logger.warning("Please add git to your $PATH")
        return {'contributors': ["I failed to construct the contributor list"]}

    contributors = re.findall(r'Author: (.* <.*@.*>)\n', log)
    return {'contributors': set(contributors)}
