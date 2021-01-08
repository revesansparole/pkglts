# {# pkglts, pysetup.kwds
# format setup arguments

from pathlib import Path

from setuptools import setup, find_packages


short_descr = "Building packages with long term support"
readme = open('README.rst').read()
history = open('HISTORY.rst').read()

# find packages
pkgs = find_packages('src')

src_dir = Path("src/pkglts")

data_files = []
for pth in src_dir.glob("**/*.*"):
    if pth.suffix in ['', '.bat', '.cfg', '.json', '.md', '.in', '.ini', '.png', '.ps1', '.rst', '.sh', '.tpl', '.txt', '.yaml', '.yml']:
        data_files.append(str(pth.relative_to(src_dir)))

pkg_data = {'pkglts': data_files}

setup_kwds = dict(
    name='pkglts',
    version="5.2.1",
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="revesansparole",
    author_email="revesansparole@gmail.com",
    url='https://github.com/revesansparole/pkglts',
    license='CeCILL-C',
    zip_safe=False,

    packages=pkgs,
    
    package_dir={'': 'src'},
    
    
    package_data=pkg_data,
    setup_requires=[
        "pytest-runner",
        ],
    install_requires=[
        "jinja2",
        "requests",
        "semver",
        "unidecode",
        ],
    tests_require=[
        "coverage",
        "coveralls",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "tox",
        ],
    entry_points={},
    keywords='packaging, package builder',
    
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    )
# #}
# change setup_kwds below before the next pkglts tag

setup_kwds['entry_points']['console_scripts'] = ['pmg = pkglts.manage_script:main']
setup_kwds['entry_points']['pkglts'] = [
    'base = pkglts.option.base.option:OptionBase',
    'appveyor = pkglts.option.appveyor.option:OptionAppveyor',
    'conda = pkglts.option.conda.option:OptionConda',
    'coverage = pkglts.option.coverage.option:OptionCoverage',
    'coveralls = pkglts.option.coveralls.option:OptionCoveralls',
    'data = pkglts.option.data.option:OptionData',
    'doc = pkglts.option.doc.option:OptionDoc',
    'flake8 = pkglts.option.flake8.option:OptionFlake8',
    'git = pkglts.option.git.option:OptionGit',
    'github = pkglts.option.github.option:OptionGithub',
    'gitlab = pkglts.option.gitlab.option:OptionGitlab',
    'landscape = pkglts.option.landscape.option:OptionLandscape',
    'lgtm = pkglts.option.lgtm.option:OptionLgtm',
    'license = pkglts.option.license.option:OptionLicense',
    'notebook = pkglts.option.notebook.option:OptionNotebook',
    'plugin_project = pkglts.option.plugin_project.option:OptionPluginProject',
    'pypi = pkglts.option.pypi.option:OptionPypi',
    'pysetup = pkglts.option.pysetup.option:OptionPysetup',
    'readthedocs = pkglts.option.readthedocs.option:OptionReadthedocs',
    'reqs = pkglts.option.reqs.option:OptionReqs',
    'requires = pkglts.option.requires.option:OptionRequires',
    'sphinx = pkglts.option.sphinx.option:OptionSphinx',
    'src = pkglts.option.src.option:OptionSrc',
    'test = pkglts.option.test.option:OptionTest',
    'tox = pkglts.option.tox.option:OptionTox',
    'travis = pkglts.option.travis.option:OptionTravis',
    'version = pkglts.option.version.option:OptionVersion',
]

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
