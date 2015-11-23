# import json
# from subprocess import call
#
# from tuto_tools import initialize
#
# initialize()
#
# with open("pkg_cfg.json", 'r') as f:
#     pkg_cfg = json.load(f)
#
# pkg_cfg['base'] = dict(pkgname='toto',
#                        namespace=None,
#                        author_name='moi',
#                        author_email='moi@gmail.com')
# pkg_cfg['doc'] = dict(description="belle petite description",
#                       keywords="keys, words")
# pkg_cfg['test'] = dict(option=None)
# pkg_cfg['license'] = dict(name="mit",
#                           year="2015",
#                           organization="oa",
#                           project="toto")
# pkg_cfg['version'] = dict(auto="off", major="0", minor="5", post="0")
# pkg_cfg['pysetup'] = dict(intended_versions=["27", "34", "35"],
#                          classifiers=["Intended Audience :: Developers"])
#
# pkg_cfg['plugin'] = dict(option=None)
#
# with open("pkg_cfg.json", 'w') as f:
#     json.dump(pkg_cfg, f)
#
# execfile("../extra_info.py")
#
# call("manage regenerate")
#
# call("manage add -opt example -e option_name base")
# call("manage add -opt example -e option_name plugin")
#
# call("manage regenerate")
#
# print "SETUP.py"
# with open("setup.py", 'r') as f:
#     print f.read()
#
# print "PLUGIN.py"
# with open("src/toto_plugin/plugin_def.py", 'r') as f:
#     print f.read()
#
# call("python setup.py develop", shell=True)
