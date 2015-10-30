from pkglts.option_tools import ask_arg


def main(pkg_cfg, extra):
    pyvers = ask_arg("pydist.intended_versions", pkg_cfg, ["27"], extra)

    classifiers = ask_arg("pydist.classifiers", pkg_cfg,
                          ["Intended Audience :: Developers"],
                          extra)

    return dict(intended_versions=pyvers,
                classifiers=classifiers)
