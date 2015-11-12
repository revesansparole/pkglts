import mock

from pkglts.option.pysetup.config import main


def test_config_is_self_sufficient():
    pkg_cfg = dict(base={'owner': 'owner'})
    # call config a first time
    cfg = main(pkg_cfg, dict(author_name='author',
                             author_email='email',
                             intended_versions=["27"],
                             classifiers=["class"]))

    # check that a second call with the same info provided
    # first does not require user input
    new_cfg = main(pkg_cfg, cfg)

    # second has not modified options
    assert cfg == new_cfg


def test_config_use_good_defaults():
    pkg_cfg = dict(base={'owner': 'owner'})
    # call config a first time
    cfg = main(pkg_cfg, dict(author_name='author',
                             author_email='email',
                             intended_versions=["27"],
                             classifiers=["class"]))

    # check that a second call provide right defaults
    pkg_cfg['pysetup'] = cfg
    with mock.patch("pkglts.option_tools.loc_input", return_value=''):
        new_cfg = main(pkg_cfg, {})
        assert cfg == new_cfg
