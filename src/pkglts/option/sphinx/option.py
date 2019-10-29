from pathlib import Path

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.small_tools import is_pathname_valid
from pkglts.version import __version__


class OptionSphinx(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        sec = dict(
            theme="default",
            autodoc_dvlpt=True,
            build_dir="build/sphinx",
            gallery="",
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        if cfg['doc']['fmt'] != 'rst':
            invalids.append('doc.fmt')

        theme = cfg[self._name]['theme']
        if theme != str(theme):
            invalids.append('sphinx.theme')

        gallery = cfg[self._name]['gallery']
        if gallery != "" and not is_pathname_valid(gallery):
            invalids.append('sphinx.gallery')

        return invalids

    def require_option(self):
        return ['pysetup']

    def require(self, cfg):
        yield Dependency('sphinx', intent='doc')
        if cfg["sphinx"]["theme"] == "sphinx_rtd_theme":
            yield Dependency('sphinx_rtd_theme', intent='doc')

        if cfg['sphinx']['gallery'] != "":
            yield Dependency('sphinx-gallery', intent='doc')
