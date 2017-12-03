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
        r_user = requests.get(contributor['url'])
        if r_user.status_code != 200:
            contributors.append('%s' % (contrib_list['login']))
        else:
            contrib_detail = r_user.json()
            contributors.append('%s, %s, <%s>' % (contrib_detail['login'], contrib_detail['name'],
                                                  contrib_detail['email']))
    return {'contributors': contributors}
