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
    try:
        log = subprocess.check_output(['git', 'log', '--all']).decode('utf-8')
    except KeyError:
        logger.warning("Please add git to your $PATH")
        return {'contributors': ["I failed to construct the contributor list"]}

    commits = log.split('commit')
    contributors = [contributor for commit in commits
                    for contributor in re.findall(r'Author: (.* <.*@.*>)\n', commit)]
    return {'contributors': set(contributors)}
