import logging
from pathlib import Path

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.version import __version__

LOGGER = logging.getLogger(__name__)


class OptionCoverage(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def require_option(self, cfg):
        return ['test']

    def require(self, cfg):
        yield Dependency('coverage', intent='test')
        if cfg['test']['suite_name'] == 'pytest':
            yield Dependency('pytest-cov', intent='test')
