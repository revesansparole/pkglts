from lice.core import generate_license, load_package_template


def generate(txt, env):
    """ Ignore txt and generate a license
    """
    del txt  # unused
    name = env['license']['name']

    ctx = dict((k, str(v)) for k, v in env['license'].items())
    tpl = load_package_template(name)

    license_txt = generate_license(tpl, ctx)
    return license_txt


def setup_handler(txt, env):
    del txt  # unused
    return '\n    license="%s",' % env['license']['name']


mapping = {"license.generate": generate,
           "license.setup": setup_handler}
