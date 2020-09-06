# -*- coding: utf-8 -*-

import logging
import time

import xbmc
import xbmcaddon

from resources.lib.memory.memory import MemoryStorage
from resources.lib.utils import kodilogging
from resources.lib.utils import kodiutils
from resources.lib.utils.jsonrpcrequests import getPlayedPercentage
# from service import server


# logger = logging.getLogger('plugin.brokenspacebars.brokenanime')
# server.run()

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()

logger.info("##### SERVICE IS TAKING CONTROL #####")
storage = MemoryStorage('ani')

def getPercentage():
    return kodiutils.kodi_json_request(getPlayedPercentage)['percentage']

while True:
    if xbmc.Player().isPlaying():
        logger.debug("Playing something!!!!")
        try:
            logger.debug(storage['current'])
        except:
            logger.debug('Exception thrown')

        logger.debug("Percentage: " + getPercentage())
    else:
        logger.debug("Not playing :(")
        # print(storage['current'])

    time.sleep(10)

