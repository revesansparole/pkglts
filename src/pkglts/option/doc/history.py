"""
This tool will try to parse all release tags to create an history of package.
"""

import logging
import os
from pathlib import Path
from functools import cmp_to_key
from getpass import getpass
from urllib.parse import quote_plus

import requests
import semver

LOGGER = logging.getLogger(__name__)


def github_tag_list(project):
    """Retrieve tag list from project.

    Notes: release tag format
        a release tag is of the form vX.X.X where
        X.X.X stands for package version

    Args:
        project (str): name of project (e.g. "revesansparole/pkglts")

    Returns:
        (dict of (str|dict)): tag name, tag info
    """
    base_url = "https://api.github.com"
    url = f"{base_url}/repos{project}/releases"
    res = requests.get(url)
    LOGGER.info("status: %s", res.status_code)
    tags = {}
    for tag in res.json():
        if tag["tag_name"].startswith("v"):
            tags[tag["tag_name"][1:]] = dict(
                name=tag["tag_name"], date=tag["created_at"][:10], title=tag["name"], body=tag["body"]
            )

    return tags


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
    base_url = f"https://{server}/api/v4/projects"
    repo_id = quote_plus(project)
    LOGGER.info("repo_id: %s", repo_id)

    url = f"{base_url}/{repo_id}/repository/tags?private_token={token}"
    LOGGER.debug("url:  %s", url)

    res = requests.get(url)
    LOGGER.debug("status: %s", res.status_code)
    tags = {}
    for tag in res.json():
        if tag["name"].startswith("v"):
            tags[tag["name"][1:]] = dict(
                name=tag["name"],
                date=tag["commit"]["committed_date"][:10],
                title=tag["message"],
                body=tag["release"]["description"],
            )

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
    if fmt not in ("md", "rst"):
        LOGGER.warning("Doc format '%s' unsupported", fmt)
    else:
        if fmt == "md":
            txt = "# History\n\n"
            for ver in ver_list:
                tag = tags[ver]
                txt += f"## {tag['name']} - <small>*({tag['date']})*</small> - {tag['title']}\n\n"
                txt += tag["body"]
                txt += "\n\n"

        else:  # fmt == "rst":
            txt = "=======\nHistory\n=======\n\n"
            for ver in ver_list:
                tag = tags[ver]
                tag_title = f"{tag['name']} - *({tag['date']})* - {tag['title']}"
                txt += tag_title + "\n"
                txt += "=" * len(tag_title) + "\n\n"
                txt += tag["body"]
                txt += "\n\n"

        root_dir = Path(".")
        for name in (f"CHANGELOG.{fmt}", f"HISTORY.{fmt}"):
            pth = root_dir / name
            if pth.exists():
                LOGGER.info("write changelog in %s", name)
                pth.write_text(txt)
                break


def action_history(cfg, **kwds):
    """Regenerate history file from tag list."""
    LOGGER.info("Reconstruct history")

    # extract release tags from versioning system
    if "git" not in cfg.installed_options():
        LOGGER.warning("Project is not under git versioning, unable to continue")
        return

    if "gitlab" in cfg.installed_options():
        server = cfg["gitlab"]["server"]
        owner = cfg["gitlab"]["owner"]
        project = cfg["gitlab"]["project"]
        token = getpass("gitlab API access token:")
        tags = gitlab_tag_list(server, f"{owner}/{project}", token)
    elif "github" in cfg.installed_options():
        owner = cfg["github"]["owner"]
        project = cfg["github"]["project"]
        tags = github_tag_list(f"{owner}/{project}")
    else:
        LOGGER.info("git only option not supported yet")
        tags = {}

    # format tags into history file
    if tags:
        write_changelog(tags, cfg["doc"]["fmt"])


def parser_history(subparsers):
    """Associate a CLI to this tool.

    Notes: The CLI will be a subcommand of pmg.

    Args:
        subparsers (ArgumentParser): entity to create a subparsers

    Returns:
        (string): a unique id for this parser
        (callable): the action to perform
    """
    subparsers.add_parser("history", help=action_history.__doc__)

    return "history", action_history
