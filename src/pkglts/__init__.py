# {{pkglts base1,
from . import version

__version__ = version.__version__
# }}

# {{pkglts base2,
'github'
# }}

import logging
import logging.handlers

fmt = logging.Formatter('%(asctime)s %(levelname)s (%(name)s): %(message)s')

wng_ch = logging.StreamHandler()
wng_ch.setLevel(logging.WARNING)
wng_ch.setFormatter(fmt)

info_ch = logging.FileHandler("info.log")
info_ch.setLevel(logging.INFO)
info_ch.setFormatter(fmt)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(wng_ch)
logger.addHandler(info_ch)
