import logging
import logging.handlers

# from os import remove, rename
# from os.path import exists


fmt = logging.Formatter('%(asctime)s %(levelname)s (%(name)s): %(message)s')

wng_ch = logging.StreamHandler()
wng_ch.setLevel(logging.WARNING)
wng_ch.setFormatter(fmt)

logger = logging.getLogger("pkglts")
logger.setLevel(logging.DEBUG)
logger.addHandler(wng_ch)

try:
    # n = 5
    # tpl = ".pkglts/info.log.%d"
    # if exists(tpl % n):
    #     remove(tpl % n)
    #
    # for i in range(n, 0, -1):
    #     if exists(tpl % (i - 1)):
    #         rename(tpl % (i - 1), tpl % i)
    #
    # if exists(".pkglts/info.log"):
    #     rename(".pkglts/info.log", tpl % 0)
    #
    # info_ch = logging.FileHandler(".pkglts/info.log", 'w')
    info_ch = logging.StreamHandler()
    info_ch.setLevel(logging.INFO)
    info_ch.setFormatter(fmt)

    logger.addHandler(info_ch)
except IOError:
    print("no info handler")
