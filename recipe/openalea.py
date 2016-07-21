from pkglts.manage_script import (action_add, action_init, action_regenerate,
                                  get_pkg_config, write_pkg_config)

action_init()
action_add("pysetup", "sphinx", "github")

env = get_pkg_config()

env.globals["base"].namespace = "openalea"
env.globals["doc"].keywords.append("openalea")
env.globals["github"].owner = "openalea"

env.globals["license"].name = "cecill-c"
env.globals["license"].organization = "openalea"
env.globals["license"].year = 2016

write_pkg_config(env)

action_regenerate()
