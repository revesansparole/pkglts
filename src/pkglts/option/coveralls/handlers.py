from pkglts.option.doc import fmt_badge


def badge(txt, env):
    del txt  # unused
    owner = env['base']['owner']
    project = env['github']['project']

    url = "coveralls.io/github/%s/%s?branch=master" % (owner, project)
    img = ("coveralls.io/repos/%s/%s/" % (owner, project) +
           "badge.svg?branch=master&service=github")
    return fmt_badge(img, url, "Coverage report status")


mapping = {'coveralls.badge': badge}
