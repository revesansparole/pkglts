from pkglts.option_tools import ask_arg


def main(pkg_cfg, extra):
    project = ask_arg('readthedocs.project',
                      pkg_cfg,
                      pkg_cfg['github']['project'],
                      extra)

    return dict(project=project)
