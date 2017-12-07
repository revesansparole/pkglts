

def environment_extensions(cfg):
    """Add more functionality to an environment.

    Args:
        cfg (Config):  current package configuration

    Returns:
        dict of str: any
    """

    if cfg['gitlab']['project_url'] == "Auto":
        if cfg['gitlab']['sub_group'] is None:
            project_loc = cfg['gitlab']['owner']
        else:
            project_loc = '%s/%s' % (cfg['gitlab']['owner'], cfg['gitlab']['sub_group'])
        url = "https://%s/%s/%s" % (cfg['gitlab']['server'], project_loc, cfg['gitlab']['project'])
    else:
        url = cfg['gitlab']['project_url']
    return {"url": url}
