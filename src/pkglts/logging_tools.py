"""
Base setting for logging in the package.
This module is executed when importing pkglts.
"""
import logging
import logging.handlers
from os import remove, rename
from os.path import exists


def rolling_logs(logger):
    """Associate log files using a rolling mechanism"""
    nb_logs = 5
    tpl = ".pkglts/info.log.%d"
    if exists(tpl % nb_logs):
        remove(tpl % nb_logs)

    for i in range(nb_logs, 0, -1):
        if exists(tpl % (i - 1)):
            rename(tpl % (i - 1), tpl % i)

    if exists(".pkglts/info.log"):
        rename(".pkglts/info.log", tpl % 0)

    info_ch = logging.FileHandler(".pkglts/info.log", 'w')
    logger.addHandler(info_ch)


def main():
    """Set logging configuration"""
    fmt = logging.Formatter('%(asctime)s %(levelname)s (%(name)s): %(message)s')

    wng_ch = logging.StreamHandler()
    wng_ch.setLevel(logging.WARNING)
    wng_ch.setFormatter(fmt)

    logger = logging.getLogger("pkglts")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(wng_ch)

    try:
        # rolling_logs(logger)
        info_ch = logging.StreamHandler()
        info_ch.setLevel(logging.INFO)
        info_ch.setFormatter(fmt)

        logger.addHandler(info_ch)
    except IOError:
        print("no info handler")


if __name__ == '__main__':
    main()
