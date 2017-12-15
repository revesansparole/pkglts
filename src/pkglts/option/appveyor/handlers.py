"""
Set of function to extend jinja2 environment.
"""
from pkglts.option.doc import fmt_badge


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    owner = cfg['github']['owner']
    project = cfg['github']['project'].replace("_", "-")
    token = cfg['appveyor']['token']

    url = "ci.appveyor.com/project/%s/%s/branch/master" % (owner, project)
    img = "ci.appveyor.com/api/projects/status/%s/branch/master?svg=true" % token
    badge = fmt_badge(img, url, "Appveyor build status", cfg['doc']['fmt'])

    return {"badge": badge}
