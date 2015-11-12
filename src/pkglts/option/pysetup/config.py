from pkglts.option_tools import ask_arg


def main(pkg_cfg, extra):
    author_name = ask_arg("pysetup.author_name", pkg_cfg,
                          pkg_cfg['base']['owner'], extra)
    author_email = ask_arg("pysetup.author_email", pkg_cfg,
                           "moi@email.com", extra)
    pyvers = ask_arg("pysetup.intended_versions", pkg_cfg, ["27"], extra)

    classifiers = ask_arg("pysetup.classifiers", pkg_cfg,
                          ["Intended Audience :: Developers"],
                          extra)

    return dict(author_name=author_name,
                author_email=author_email,
                intended_versions=pyvers,
                classifiers=classifiers)
