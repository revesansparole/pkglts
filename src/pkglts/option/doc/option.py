from pathlib import Path

from pkglts.dependency import Dependency
from pkglts.option_object import Option
from pkglts.option_tools import available_options
from pkglts.version import __version__

from . import history


class OptionDoc(Option):
    def version(self):
        return __version__

    def root_dir(self):
        return Path(__file__).parent

    def update_parameters(self, cfg):
        sec = dict(
            description="belle petite description",
            fmt="rst",
            keywords=[]
        )
        cfg[self._name] = sec

    def check(self, cfg):
        invalids = []
        description = cfg[self._name]['description']
        fmt = cfg[self._name]['fmt']
        # keywords = env.globals['doc'].keywords

        if not description:
            invalids.append("doc.description")

        if fmt not in ('rst', 'md'):
            invalids.append("doc.fmt")

        return invalids

    def require_option(self):
        return ['base']

    def require(self, cfg):
        if cfg[self._name]['fmt'] == 'md':
            yield Dependency('mkdocs', intent='doc')

    def environment_extensions(self, cfg):
        badges = []
        for name in sorted(set(cfg.installed_options()) - {self._name}):
            opt = available_options[name]
            ext = opt.environment_extensions(cfg)
            if 'badge' in ext:
                badges.append(ext['badge'])
            if 'badges' in ext:
                badges.extend(ext['badges'])

        return {"badges": badges}

    def tools(self, cfg):
        del cfg
        yield history.parser_history
