# -*- coding: utf-8 -*-

import logging
import time
import json

import xbmc
import xbmcaddon

from resources.lib.memory.memory import MemoryStorage
from resources.lib.utils import kodilogging
from resources.lib.utils.kodiutils import kodi_json_request
from resources.lib.utils.jsonrpcrequests import getPlayedPercentage
from resources.lib.anilist.anilist import update_anime
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
    # if 'episode' in storage['current'].keys():
    if storage['current']['requireCheck']:
        if int(storage['current']['progress']) < int(storage['current']['episode']):
            logger.debug("We will update")
            return True
        else:
            logger.debug("No need to update")
            return False
    else:
        logger.debug("Not ready yet")
        return None

while True:
    # Check if there is a storage item loaded
    try:
        requireCheck = storage['current']['requireCheck']
    except:
        logger.debug("Nothing requires updating, waiting")
        time.sleep(10)
        continue

    # If something is loaded and playing
    if xbmc.Player().isPlaying() and requireCheck:
        logger.debug("Playing something from brokenanime!!!!")
        # try:
        #     logger.debug(storage)
        # except:
        #     logger.debug('Exception thrown')

        if doesItRequireUpdate():
            if (getPercentage() > 70.0):
                # Make the update call
                resp = update_anime(storage['current']['anime_id'], storage['current']['episode'])
                logger.debug("Updated anilist: " + json.dumps(resp))
                # Update requiredCheck if successful
                store = storage['current']
                store['requireCheck'] = False
                storage['current'] = store
                # logger.debug("I will update")
                # pass
            else:
                logger.debug("Not ready to update yet")
        else:
            # Update requiredCheck to save checks
            store = storage['current']
            store['requireCheck'] = False
            storage['current'] = store
    else:
        logger.debug("Not playing or no update is needed")
        # print(storage['current'])

    time.sleep(10)

