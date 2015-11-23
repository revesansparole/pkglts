import logging
import logging.handlers

fmt = logging.Formatter('%(asctime)s %(levelname)s (%(name)s): %(message)s')

wng_ch = logging.StreamHandler()
wng_ch.setLevel(logging.WARNING)
wng_ch.setFormatter(fmt)

logger = logging.getLogger("pkglts")
logger.setLevel(logging.DEBUG)
logger.addHandler(wng_ch)

try:
    info_ch = logging.FileHandler(".pkglts/info.log")
    info_ch.setLevel(logging.INFO)
    info_ch.setFormatter(fmt)

    logger.addHandler(info_ch)
except IOError:
    print("no info handler")
