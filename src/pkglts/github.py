""" All github related functions.
"""

import json
from github3 import GitHubError, login
from os.path import exists

from .option_tools import ask_arg


def ensure_login(pkg_cfg, recursion_ind=0):
    """ Check that the user is logged to github.

    Look for an already registered user. If none found
    ask for credentials and open a new session.
    """
    if recursion_ind > 3:
        raise UserWarning("Pb, infinite recursion in github login")

    cfg = pkg_cfg['github']
    owner = pkg_cfg['base']['owner']
    project = cfg['project']

    try:
        gh = pkg_cfg['_session']['github']
        try:
            repo = pkg_cfg['_session']['github_repo']
            return gh, repo
        except KeyError:
            try:
                repo = gh.repository(owner, project)
                pkg_cfg['_session']['github_repo'] = repo
                return gh, repo
            except GitHubError:
                print ("bad credentials")
                del pkg_cfg['_session']['github']
                return ensure_login(pkg_cfg, recursion_ind + 1)

    except KeyError:
        pass

    if exists(".cookie.json"):
        with open(".cookie.json", 'r') as f:
            cookie = json.load(f)
    else:
        cookie = {}

    if 'login' in cookie:
        user = cookie['login']
    else:
        user = ask_arg("github.user", pkg_cfg, owner, cfg)
        if user == "":
            print("anonymous forbidden")
            return ensure_login(pkg_cfg, recursion_ind + 1)

    if 'password' in cookie:
        pwd = cookie['password']
    else:
        pwd = ask_arg("github.password", pkg_cfg, "", cfg)
        if pwd == "":
            print("need your password, sorry")
            return ensure_login(pkg_cfg, recursion_ind + 1)

    gh = login(user, pwd)
    try:
        repo = gh.repository(owner, project)
    except GitHubError:
        print ("bad credentials")
        return ensure_login(pkg_cfg, recursion_ind + 1)

    if '_session' not in pkg_cfg:
        pkg_cfg['_session'] = {}

    pkg_cfg['_session']['github'] = gh
    pkg_cfg['_session']['github_repo'] = repo

    return gh, repo


def fetch_contributors(pkg_cfg):
    """ Try to list all contributors for a github project
    """
    gh, repo = ensure_login(pkg_cfg)

    info = []
    for user in repo.contributors():
        name = user.name
        if len(name) == 0:
            name = user.login

        info.append((name, user.email))

    return info


def fetch_history(pkg_cfg):
    """ Get the list of commit messages
    """
    gh, repo = ensure_login(pkg_cfg)

    info = []
    # TODO

    return info
