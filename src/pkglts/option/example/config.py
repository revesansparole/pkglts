from pkglts.local import load_all_handlers
from pkglts.manage_tools import check_tempering, regenerate_dir
from pkglts.option_tools import ask_arg, get_user_permission


def main(pkg_cfg, extra):
    option = ask_arg("option_name", {}, "base", extra)

    if option is None:
        return None

    if option not in pkg_cfg:
        print("please install option before example files")
        return None

    # get handlers
    h = load_all_handlers(pkg_cfg)

    root = "pkglts_data/example/%s" % option
    # walk all files in example repo to check for possible tempering
    # of files by user
    tf = []
    check_tempering(root, ".", h, pkg_cfg, tf)
    overwrite = {}
    if len(tf) > 0:
        print("Trying to overwrite files that already exists")
        for name in tf:
            overwrite[name] = get_user_permission("overwrite '%s'" % name,
                                                  False)

    if '_session' not in pkg_cfg:
        pkg_cfg['_session'] = {}

    pkg_cfg['_session']['overwrite'] = overwrite
    # get option examples
    regenerate_dir(root, ".", h, pkg_cfg, False)

    return None
