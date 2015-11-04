from pkglts.option.doc import fmt_badge


def badge(txt, env):
    owner = env['base']['owner']
    project = env['github']['project']

    url = "landscape.io/github/%s/%s/master" % (owner, project)
    img = url + "/landscape.svg?style=flat"
    return fmt_badge(img, url, "Code health status")


mapping = {'landscape.badge': badge}
