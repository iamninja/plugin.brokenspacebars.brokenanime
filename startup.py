# -*- coding: utf-8 -*-

import logging
import time

import xbmc
import xbmcaddon

from resources.lib.memory.memory import MemoryStorage
from resources.lib.utils import kodilogging
from resources.lib.utils.kodiutils import kodi_json_request
from resources.lib.utils.jsonrpcrequests import getPlayedPercentage
# from service import server

# TODO: This file probably need to be kept at a minimum.
# TODO: Smarter loop to get a smaller footprint.
# TODO: Check if it is possible to have an event driven service.

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()

logger.info("##### SERVICE IS TAKING CONTROL #####")
storage = MemoryStorage('ani')

def getPercentage():
    resp = kodi_json_request(getPlayedPercentage)
    # logger.debug(resp['percentage'])
    return resp['percentage']

def doesItRequireUpdate():
    if 'episode' in storage['current'].keys():
        if int(storage['current']['progress']) < int(storage['current']['episode']):
            logger.debug("We will need to update")
            return True
        else:
            logger.debug("No need to update")
            return False
    else:
        logger.debug("Not ready yet")
        return None

while True:
    if xbmc.Player().isPlaying():
        logger.debug("Playing something!!!!")
        try:
            logger.debug(storage)
        except:
            logger.debug('Exception thrown')

        doesItRequireUpdate()

        logger.debug(getPercentage())
    else:
        logger.debug("Not playing :(")
        # print(storage['current'])

    time.sleep(10)

