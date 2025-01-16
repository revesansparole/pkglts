from copy import deepcopy

from pkglts.config_management import Config


def test_pkg_url_empty_default():
    cfg = Config(dict(pyproject={"intended_versions": ["2.7"]}))
    cfg.load_extra()
    assert len(cfg._env.globals["pyproject"].urls) == 0


def test_pkg_url_look_multiple_places():
    tpl_cfg = dict(
        base={"pkgname": "toto", "namespace": "oa", "url": None},
        doc={"fmt": "rst"},
        github={"url": None, "project": "project", "owner": "toto"},
        gitlab={"url": None, "project": "project", "owner": "toto"},
        pypi={"classifiers": [], "servers": [dict(name="pypi", url="https://upload.pypi.org/legacy/")]},
        readthedocs={"project": "project"},
        pyproject={"intended_versions": ["2.7"]},
    )

    for name in ("base", "github", "gitlab"):  # TODO, "pypi", "readthedocs"):
        loc_cfg = deepcopy(tpl_cfg)
        loc_cfg[name]["url"] = name
        cfg = Config(loc_cfg)
        cfg.load_extra()
        assert any(name in url for url in cfg._env.globals["pyproject"].urls.values())


def test_py_max_ver_uses_max_intended_version():
    cfg = Config(dict(pyproject={"intended_versions": ["2.7"]}))
    cfg.load_extra()
    assert cfg._env.globals["pyproject"].py_max_ver == "2.7"

    cfg = Config(dict(pyproject={"intended_versions": ["2.7", "3.6"]}))
    cfg.load_extra()
    assert cfg._env.globals["pyproject"].py_max_ver == "3.6"

    cfg = Config(dict(pyproject={"intended_versions": ["3.7", "3.6"]}))
    cfg.load_extra()
    assert cfg._env.globals["pyproject"].py_max_ver == "3.7"

    cfg = Config(dict(pyproject={"intended_versions": ["3.10", "3.9"]}))
    cfg.load_extra()
    assert cfg._env.globals["pyproject"].py_max_ver == "3.10"


def test_py_min_ver_uses_min_intended_version():
    cfg = Config(dict(pyproject={"intended_versions": ["2.7"]}))
    cfg.load_extra()
    assert cfg._env.globals["pyproject"].py_min_ver == "2.7"

    cfg = Config(dict(pyproject={"intended_versions": ["2.7", "3.6"]}))
    cfg.load_extra()
    assert cfg._env.globals["pyproject"].py_min_ver == "2.7"

    cfg = Config(dict(pyproject={"intended_versions": ["3.6", "3.7"]}))
    cfg.load_extra()
    assert cfg._env.globals["pyproject"].py_min_ver == "3.6"

    cfg = Config(dict(pyproject={"intended_versions": ["3.9", "3.10"]}))
    cfg.load_extra()
    assert cfg._env.globals["pyproject"].py_min_ver == "3.9"
