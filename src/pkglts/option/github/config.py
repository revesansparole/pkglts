from pkglts.option_tools import ask_arg


def main(pkg_cfg, extra):
    project = ask_arg("github.project",
                      pkg_cfg,
                      pkg_cfg['base']['pkgname'],
                      extra)

    return dict(project=project)
