import logging
import re
import subprocess
from pathlib import Path

from pkglts.option_object import Option
from pkglts.version import __version__
from unidecode import unidecode

LOGGER = logging.getLogger(__name__)


class OptionGit(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self):
        return ['base']

    def environment_extensions(self, cfg):
        del cfg

        try:
            log = subprocess.check_output(['git', 'log', '--all', '--use-mailmap'],
                                          stderr=subprocess.STDOUT).decode('utf-8')
            commiters = re.findall(r'Author: (.* <.*@.*>)\n', unidecode(log))
            ccs = [(commiters.count(name), name) for name in set(commiters)]
            contributors = [name for nb, name in sorted(ccs, reverse=True)]
        except (KeyError, OSError):
            LOGGER.warning("Please add git to your $PATH")
            contributors = ["I failed to construct the contributor list"]
        except subprocess.CalledProcessError as err:
            contributors = [f"Pb with git, {err}"]

        return {'contributors': contributors}
