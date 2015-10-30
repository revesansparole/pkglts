from pkglts.option_tools import ask_arg


def main(pkg_cfg, extra):
    name = ask_arg("license.name", pkg_cfg, 'mit', extra)
    year = ask_arg("license.year", pkg_cfg, 2015, extra)
    organization = ask_arg("license.organization", pkg_cfg, "oa", extra)
    project = ask_arg("license.project",
                      pkg_cfg,
                      pkg_cfg['base']['pkgname'],
                      extra)

    return dict(name=name.strip(),
                year=year,
                organization=organization,
                project=project)
