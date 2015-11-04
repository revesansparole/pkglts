from argparse import ArgumentParser

from local import installed_options
from manage import (clean, get_pkg_config,
                    init_pkg, install_example_files,
                    regenerate,
                    add_option, edit_option,
                    update_option, update_pkg,
                    write_pkg_config)


def main():
    parser = ArgumentParser(description='Package structure manager')
    parser.add_argument('action', metavar='action',
                        help="action to perform on package")

    parser.add_argument('-opt', '--option', metavar='option_name',
                        help="argument for action=add", dest='option')

    parser.add_argument('-e', metavar='extra', nargs=2, action='append',
                        help='extra arguments to pass to the action',
                        dest='extra')

    args = parser.parse_args()
    if args.extra is None:
        extra = {}
    else:
        extra = dict(args.extra)

    if args.action == 'init':
        print "init package"
        init_pkg()
    elif args.action == 'clean':
        clean()
    elif args.action == 'update':
        pkg_cfg = get_pkg_config()
        if args.option is None:
            print "update package"
            pkg_cfg = update_pkg(pkg_cfg)
        elif args.option == 'all':
            print "update all options"
            for name in installed_options(pkg_cfg):
                pkg_cfg = update_option(name, pkg_cfg)
        else:
            print "update option"
            pkg_cfg = update_option(args.option, pkg_cfg)
        write_pkg_config(pkg_cfg)
    elif args.action in ('rg', 'regenerate'):
        print "regenerate"
        overwrite = 'overwrite' in extra
        pkg_cfg = get_pkg_config()
        clean()
        regenerate(pkg_cfg, overwrite=overwrite)
        write_pkg_config(pkg_cfg)
    elif args.action == 'add':
        pkg_cfg = get_pkg_config()
        pkg_cfg = add_option(args.option, pkg_cfg, extra)
        write_pkg_config(pkg_cfg)
    elif args.action == 'edit':
        pkg_cfg = get_pkg_config()
        pkg_cfg = edit_option(args.option, pkg_cfg)
        write_pkg_config(pkg_cfg)
    elif args.action == 'example':
        pkg_cfg = get_pkg_config()
        install_example_files(args.option, pkg_cfg)
    else:
        print "unknown"


if __name__ == '__main__':
    main()
