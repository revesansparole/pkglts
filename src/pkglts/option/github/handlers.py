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
        log = subprocess.check_output(['git', 'log', '--all', '--use-mailmap']).decode('utf-8')
        contributors = re.findall(r'Author: (.* <.*@.*>)\n', log)
    except KeyError:
        logger.warning("Please add git to your $PATH")
        contributors = ["I failed to construct the contributor list"]
    except subprocess.CalledProcessError as e:
        contributors = ["Pb with git, %s" % str(e)]
    
    return {'contributors': set(contributors)}
