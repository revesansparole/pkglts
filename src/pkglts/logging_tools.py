"""
Base setting for logging in the package.
This module is executed when importing pkglts.
"""
import logging
import logging.handlers

from .config import pkglts_dir


def rolling_logs(logger):
    """Associate log files using a rolling mechanism"""
    nb_logs = 5
    tpl = pkglts_dir / "info.log.%d"
    pth = pkglts_dir / f"info.{nb_logs:d}.log"
    if pth.exists():
        pth.unlink()

    for i in range(nb_logs, 0, -1):
        pth = pkglts_dir / f"info.{i - 1:d}.log"
        if pth.exists():
            pth.rename(pkglts_dir / f"info.{i:d}.log")

    pth = pkglts_dir / "info.log"
    if pth.exists():
        pth.rename(tpl % 0)

    info_ch = logging.FileHandler(str(pth), 'w')
    logger.addHandler(info_ch)


def main(verbosity):
    """Set logging configuration.

    Args:
        verbosity (int): verbosity level

    Returns:
        None
    """
    if verbosity > 2:
        verbosity = 2
    vlevel = [logging.WARNING, logging.INFO, logging.DEBUG][verbosity]

    fmt = logging.Formatter('%(asctime)s %(levelname)s (%(name)s): %(message)s')

    wng_ch = logging.StreamHandler()
    wng_ch.setLevel(vlevel)
    wng_ch.setFormatter(fmt)

    logger = logging.getLogger("pkglts")
    logger.setLevel(vlevel)
    logger.addHandler(wng_ch)

    # try:
    #     # rolling_logs(logger)
    #     info_ch = logging.StreamHandler()
    #     info_ch.setLevel(logging.INFO)
    #     info_ch.setFormatter(fmt)
    #
    #     logger.addHandler(info_ch)
    # except IOError:
    #     print("no info handler")


if __name__ == '__main__':
    main(0)
