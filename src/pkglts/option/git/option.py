import logging
import re
import subprocess
from pathlib import Path

from unidecode import unidecode

from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionGit(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        LOGGER.info("update parameters %s", self._name)
        sec = dict(
            permanent_branches=[],
        )
        cfg[self._name] = sec

    def require_option(self, cfg):
        return ['base']

    def environment_extensions(self, cfg):
        del cfg

        try:
            log = subprocess.check_output(['git', 'log', '--all', '--use-mailmap'],
                                          stderr=subprocess.STDOUT).decode('utf-8')
            commiters = re.findall(r'Author: (.*) <(.*@.*)>\n', unidecode(log))
            ccs = [(commiters.count(commiter), commiter) for commiter in set(commiters)]
            contributors = [(cmt_name.replace("\\", "/"), cmt_email)
                            for nb, (cmt_name, cmt_email) in sorted(ccs, reverse=True)]
        except (KeyError, OSError):
            LOGGER.warning("Please add git to your $PATH")
            contributors = [("I failed to construct the contributor list", "")]
        except subprocess.CalledProcessError as err:
            contributors = [(f"Pb with git, {err}", "err@err.err")]

        return {'contributors': contributors}
