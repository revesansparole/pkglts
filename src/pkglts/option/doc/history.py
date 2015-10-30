from pkglts.github import fetch_history


def history(txt, env):
    if 'github' in env:
        print("fetch history on github")
        info = fetch_history(env)
        if info is not None:
            items = ["  * %s" % it for it in info]
            return "\n".join(items)

    return txt
