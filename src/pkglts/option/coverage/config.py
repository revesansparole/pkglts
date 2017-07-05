from pkglts.dependency import Dependency

parameters = []


def require(purpose, env):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        env (jinja2.Environment):  current working environment

    Returns:
        (list of Dependency)
    """
    if purpose == 'option':
        options = ['test']
        return [Dependency(name) for name in options]

    if purpose == 'dvlpt':
        deps = [Dependency('coverage')]
        test_suite = env.globals['test'].suite_name
        if test_suite == 'pytest':
            deps.append(Dependency('pytest-cov'))

        return deps

    return []
