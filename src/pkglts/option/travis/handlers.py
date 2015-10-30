
def pyversions(txt, env):
    intended_versions = env['pydist']['intended_versions']
    items = ['   - "%s.%s"' % (ver[0], ver[1]) for ver in intended_versions]
    return "\n".join(items)


mapping = {'travis.pyversions': pyversions}
