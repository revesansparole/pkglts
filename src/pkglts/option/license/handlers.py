from lice.core import generate_license, load_package_template


def generate(txt, env):
    """ Ignore txt and generate a license
    """
    name = env['license']['name']

    ctx = env['license']
    tpl = load_package_template(name)

    license_txt = generate_license(tpl, ctx)
    return license_txt


def setup_handler(txt, env):
    return 'license="%s",' % env['license']['name']


mapping = {"license.generate": generate,
           "license.setup": setup_handler}
