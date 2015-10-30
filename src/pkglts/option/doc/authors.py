from pkglts.github import fetch_contributors


def leading_list(txt, env):
    if 'github' in env:
        print("fetch authors on github")
        contributors = fetch_contributors(env)
        if contributors is not None:
            items = ["  * %s <%s>" % it for it in contributors]

            return "\n".join(items)

    return txt


def contributing_list(txt, env):
    return txt
