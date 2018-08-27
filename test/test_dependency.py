from pkglts.dependency import Dependency


def test_dependency_respect_strict_pkg_mng():
    # conda
    dep = Dependency("toto", pkg_mng="conda")
    assert dep.is_conda(strict=True)
    assert dep.is_conda(strict=False)
    dep = Dependency("toto", pkg_mng=None)
    assert not dep.is_conda(strict=True)
    assert dep.is_conda(strict=False)
    dep = Dependency("toto", pkg_mng="pip")
    assert not dep.is_conda(strict=True)
    assert not dep.is_conda(strict=False)
    dep = Dependency("toto", pkg_mng="git+https://")
    assert not dep.is_conda(strict=True)
    assert not dep.is_conda(strict=False)
    
    # pip
    dep = Dependency("toto", pkg_mng="pip")
    assert dep.is_pip(strict=True)
    assert dep.is_pip(strict=False)
    dep = Dependency("toto", pkg_mng=None)
    assert not dep.is_pip(strict=True)
    assert dep.is_pip(strict=False)
    dep = Dependency("toto", pkg_mng="conda")
    assert not dep.is_pip(strict=True)
    assert not dep.is_pip(strict=False)
    dep = Dependency("toto", pkg_mng="git+https://")
    assert not dep.is_pip(strict=True)
    assert not dep.is_pip(strict=False)


def test_dependency_writes_correct_pip_requirements():
    # no version specified
    dep = Dependency("toto", pkg_mng="pip")
    txt = dep.fmt_pip_requirement()
    assert txt == "toto"
    txt = dep.fmt_pip_requirement(extended=True)
    assert txt == "toto  # pip install toto"

    # version fully specified without comparison indicator
    dep = Dependency("toto", pkg_mng="pip", version="2.18.0")
    txt = dep.fmt_pip_requirement()
    assert txt == "toto==2.18.0"
    txt = dep.fmt_pip_requirement(extended=True)
    assert txt == "toto==2.18.0  # pip install toto==2.18.0"

    # version partially specified without comparison indicator
    dep = Dependency("toto", pkg_mng="pip", version="2.18")
    txt = dep.fmt_pip_requirement()
    assert txt == "toto>=2.18, <2.19"
    txt = dep.fmt_pip_requirement(extended=True)
    assert txt == "toto>=2.18, <2.19  # pip install toto>=2.18, <2.19"

    # version specified with comparison indicator
    dep = Dependency("toto", pkg_mng="pip", version="==2.18")
    txt = dep.fmt_pip_requirement()
    assert txt == "toto==2.18"
    txt = dep.fmt_pip_requirement(extended=True)
    assert txt == "toto==2.18  # pip install toto==2.18"

    # no version specified conda manager
    dep = Dependency("toto", pkg_mng="conda")
    txt = dep.fmt_pip_requirement()
    assert txt == "toto"
    txt = dep.fmt_pip_requirement(extended=True)
    assert txt == "toto  # conda install toto"

    # version fully specified without comparison indicator conda manager
    dep = Dependency("toto", pkg_mng="conda", version="2.18.1")
    txt = dep.fmt_pip_requirement()
    assert txt == "toto==2.18.1"
    txt = dep.fmt_pip_requirement(extended=True)
    assert txt == "toto==2.18.1  # conda install toto=2.18.1"
    
    # version partially specified without comparison indicator conda manager
    dep = Dependency("toto", pkg_mng="conda", version="2.18")
    txt = dep.fmt_pip_requirement()
    assert txt == "toto>=2.18, <2.19"
    txt = dep.fmt_pip_requirement(extended=True)
    assert txt == "toto>=2.18, <2.19  # conda install toto=2.18"


def test_dependency_writes_correct_conda_requirements():
    # no version specified
    dep = Dependency("toto", pkg_mng="conda")
    txt = dep.fmt_conda_requirement()
    assert txt == "toto"

    # version partially specified no comparison operator
    dep = Dependency("toto", pkg_mng="conda", version="2.18")
    txt = dep.fmt_conda_requirement()
    assert txt == "toto=2.18"

    # version fully specified no comparison operator
    dep = Dependency("toto", pkg_mng="conda", version="2.18.1")
    txt = dep.fmt_conda_requirement()
    assert txt == "toto=2.18.1"

    # version specified conda comparison operator
    dep = Dependency("toto", pkg_mng="conda", version="=2.18")
    txt = dep.fmt_conda_requirement()
    assert txt == "toto=2.18"

    # version specified pip comparison operator
    dep = Dependency("toto", pkg_mng="conda", version="==2.18")
    txt = dep.fmt_conda_requirement()
    assert txt == "toto=2.18"

    # no version specified pip pkg_mng
    dep = Dependency("toto", pkg_mng="pip")
    txt = dep.fmt_conda_requirement()
    assert txt == "toto"

    # version partially specified no comparison operator pip pkg_mng
    dep = Dependency("toto", pkg_mng="pip", version="2.18")
    txt = dep.fmt_conda_requirement()
    assert txt == "toto=2.18"

    # version partially specified pip comparison operator pip pkg_mng
    dep = Dependency("toto", pkg_mng="pip", version="==2.18")
    txt = dep.fmt_conda_requirement()
    assert txt == "toto=2.18"
