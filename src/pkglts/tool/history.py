"""
This tool will try to parse all release tags to create an history of package.
"""
from functools import cmp_to_key
import logging
import os
from urllib.parse import quote_plus

import requests
import semver

from ..config_management import get_pkg_config

logger = logging.getLogger(__name__)


def gitlab_tag_list(server, project, token):
    """Retrieve tag list from project.
    
    Notes: release tag format
        a release tag is of the form vX.X.X where
        X.X.X stands for package version
    
    Args:
        server (str): base url of gitlab server (e.g. "framagit.org")
        project (str): name of project (e.g. "agro/agrosim")
        token (str): valid token to access project repo

    Returns:
        (dict of (str|dict)): tag name, tag info
    """
    base_url = "https://%s/api/v4/projects/" % server
    repo_id = quote_plus(project)
    print("repo_id", repo_id)
    
    url = base_url + repo_id + "/repository/tags" + "?private_token={}".format(token)
    print("url", url)
    
    r = requests.get(url)
    print("status", r.status_code)
    tags = {}
    for tag in r.json():
        if tag['name'].startswith("v"):
            tags[tag['name'][1:]] = dict(name=tag['name'],
                                         date=tag['commit']['committed_date'][:10],
                                         title=tag['message'],
                                         body=tag['release']['description'])
    
    return tags


def write_changelog(tags, fmt):
    """Write changelog file according to the content of release tags.
    
    Notes: release tag format
        a release tag is of the form vX.X.X where
        X.X.X stands for package version
    
    Warnings: invalid tags
        The process will not check that tags are properly formatted.
    
    Args:
        tags (dict): as returned by one of tag_list function
        fmt (str): format for documentation 'md' or 'rst'

    Returns:
        (None)
    """
    ver_list = list(tags.keys())
    ver_list.sort(key=cmp_to_key(semver.compare), reverse=True)
    
    # format changelog
    if fmt == "md":
        txt = "# History\n\n"
        for ver in ver_list:
            tag = tags[ver]
            txt += "## %s - <small>*(%s)*</small> - %s\n\n" % (tag['name'], tag['date'], tag['title'])
            txt += tag['body']
            txt += "\n\n"
        
        for name in ("CHANGELOG.md", "HISTORY.md"):
            if os.path.exists(name):
                logger.info("write changelog in {}".format(name))
                with open(name, 'w') as f:
                    f.write(txt)
    
    elif fmt == "rst":
        txt = "=======\nHistory\n=======\n\n"
        for ver in ver_list:
            tag = tags[ver]
            tag_title = "%s - *(%s)* - %s" % (tag['name'], tag['date'], tag['title'])
            txt += tag_title + "\n"
            txt += "=" * len(tag_title) + "\n\n"
            txt += tag['body']
            txt += "\n\n"
        
        for name in ("CHANGELOG.rst", "HISTORY.rst"):
            if os.path.exists(name):
                logger.info("write changelog in {}".format(name))
                with open(name, 'w') as f:
                    f.write(txt)
    else:
        logger.warning("Doc format '%s' unsupported" % fmt)


def action_history(*args, **kwds):
    """Regenerate history file from tag list.
    """
    del args, kwds  # unused
    
    logger.info("Reconstruct history")
    cfg = get_pkg_config()
    
    # extract release tags from versioning system
    if 'git' not in cfg.installed_options():
        logger.warning("Project is not under git versioning, unable to continue")
        return
    
    if 'gitlab' in cfg.installed_options():
        server = cfg['gitlab']['server']
        owner = cfg['gitlab']['owner']
        project = cfg['gitlab']['project']
        tags = gitlab_tag_list(server, "%s/%s" % (owner, project), "URFqxvqV8Zn51qsZGSNZ")
    elif 'github' in cfg.installed_options():
        logger.info("Github option not supported yet")
        tags = {}
    else:
        logger.info("git only option not supported yet")
        tags = {}
    
    # format tags into history file
    if len(tags) > 0:
        write_changelog(tags, cfg['doc']['fmt'])
