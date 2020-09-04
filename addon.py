# -*- coding: utf-8 -*-

from resources.lib.utils import kodilogging
from resources.lib import plugin
from resources.lib.memory.memory import MemoryStorage

import logging
import xbmcaddon
# from xbmc import translatePath

# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this
ADDON = xbmcaddon.Addon()
# PROFILE = translatePath(ADDON.getAddonInfo('profile')).decode('utf-8')
kodilogging.config()

logging.getLogger().debug("START ADDON")

storage = MemoryStorage('foo')
storage['bar'] = 'secret'

plugin.run()


