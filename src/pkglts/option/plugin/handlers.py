from os.path import splitext

from .tools import refresh_plugin_cache


def setup_handler(txt, env):
    """ Find all objects defined as plugins and install them
    as entry points
    """
    entry_point = refresh_plugin_cache(env)
    # construct entry_points txt
    entry_points_msg = ["entry_points={"]
    for gr, plugins in entry_point.items():
        entry_points_msg.append(" " * 8 + "'%s': [" % gr)
        for name, plugin_pth, obj_name in plugins:
            pkg = splitext(plugin_pth)[0][4:].replace("/", ".")
            plugin_id = pkg + ":" + obj_name
            entry_points_msg.append(" " * 12 + "'%s = %s'," % (name, plugin_id))
        entry_points_msg.append(" " * 8 + "],")

    entry_points_msg.append(" " * 4 + "},")

    return "\n".join(entry_points_msg)


mapping = {"plugin.setup": setup_handler}
