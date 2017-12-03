import requests


def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """
    owner = cfg['github']['owner']
    project = cfg['github']['project']
    url = "https://api.github.com/repos/%s/%s/contributors" % (owner, project)

    r = requests.get(url)
    if r.status_code != 200:
        return {'contributors': ["I failed to download the contributor list"]}

    contrib_list = r.json()
    contributors = []
    for contributor in contrib_list:
        contributors.append('%s, %s' % (contributor['login'], contributor['html_url']))
    return {'contributors': contributors}
