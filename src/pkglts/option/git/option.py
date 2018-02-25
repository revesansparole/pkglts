import logging
import re
import subprocess
from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from unidecode import unidecode

LOGGER = logging.getLogger(__name__)


class OptionGit(Option):
    def root_dir(self):
        return dirname(__file__)

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['base']
            return [Dependency(name) for name in options]

        return []

    def environment_extensions(self, cfg):
        del cfg

        try:
            log = subprocess.check_output(['git', 'log', '--all', '--use-mailmap']).decode('utf-8')
            commiters = re.findall(r'Author: (.* <.*@.*>)\n', unidecode(log))
            ccs = [(commiters.count(name), name) for name in set(commiters)]
            contributors = [name for nb, name in sorted(ccs, reverse=True)]
        except (KeyError, OSError):
            LOGGER.warning("Please add git to your $PATH")
            contributors = ["I failed to construct the contributor list"]
        except subprocess.CalledProcessError as err:
            contributors = ["Pb with git, %s" % str(err)]

        return {'contributors': contributors}
