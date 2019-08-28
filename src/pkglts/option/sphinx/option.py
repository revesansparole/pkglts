from os.path import dirname, exists

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.version import __version__


class OptionSphinx(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return dirname(__file__)

    def update_parameters(self, cfg):
        sec = dict(
            theme="default",
            autodoc_dvlpt=True,
            build_dir="build/sphinx",
            gallery="",
        )
        cfg['sphinx'] = sec

    def check(self, cfg):
        invalids = []
        if cfg['doc']['fmt'] != 'rst':
            invalids.append('doc.fmt')

        theme = cfg['sphinx']['theme']
        if theme != str(theme):
            invalids.append('sphinx.theme')

        gallery = cfg['sphinx']['gallery']
        if gallery != "" and not exists(gallery):
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
