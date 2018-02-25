from os.path import dirname

from pkglts.dependency import Dependency
from pkglts.option.doc import fmt_badge
from pkglts.option_object import Option


class OptionCoveralls(Option):
    def root_dir(self):
        return dirname(__file__)

    def require(self, purpose, cfg):
        del cfg

        if purpose == 'option':
            options = ['coverage', 'travis']
            return [Dependency(name) for name in options]

        if purpose == 'dvlpt':
            return [Dependency('coveralls', pkg_mng='pip')]

        return []

    def environment_extensions(self, cfg):
        owner = cfg['github']['owner']
        project = cfg['github']['project']

        url = "coveralls.io/github/%s/%s?branch=master" % (owner, project)
        img = ("coveralls.io/repos/github/%s/%s/" % (owner, project) +
               "badge.svg?branch=master")
        badge = fmt_badge(img, url, "Coverage report status", cfg['doc']['fmt'])

        return {"badge": badge}
