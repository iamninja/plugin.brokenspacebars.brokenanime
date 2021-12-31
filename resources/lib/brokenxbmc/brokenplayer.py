# -*- coding: utf-8 -*-
import logging

import xbmc
from xbmcgui import ListItem
from xbmcplugin import setResolvedUrl
import xbmcaddon

from resources.lib.anilist.anilist import update_anime

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))

class BrokenPlayer(xbmc.Player):
    def __init__(self):
        self.playback_started = False
        self.AVStarted = False
        self.anilist_scrobbling_enabled = True
        self.anilist_scrobbled = False
        self.mark_watched = False
        self.media_length = 0
        self.current_time = 0
        self.ani_storage = {}
        logger.debug("BROKENPLAYER INITIATED")
        xbmc.Player.__init__(self)

    def onAVStarted(self):
        logger.debug("-----------------------BrokenPlayer started!!")
        # self.getAnimeInfoFromStorage()

    def onPlayBackStarted(self):
        logger.debug("-----------------------BrokenPlayer started!!")



    def onPlayBackStopped(self):
        logger.debug("-----------------------BrokenPlayer stopped!!")

    def onPlayBackPaused(self):
        logger.debug("-----------------------BrokenPlayer paused!!")

    def start_playback(self):
        try:
            if self.playback_started:
                return

            self.playback_started = True
            self.anilist_scrobbled = False

            self.media_length = self.getTotalTime()

            logger.debug("----------In start_playback----------")

        except:
            import traceback
            traceback.print_exc()
            pass

    def play_source(self, link, handle, args, resume_time=None):
        if link is None:
            raise Exception

        item = ListItem(path=link)
        # args['info']['FileNameAndPath'] = link
        # item.setInfo(type='video', infoLabels=args['info'])
        item.setInfo(type='video', infoLabels={})
        # item.setArt(args['art'])
        item.setProperty('isFolder', 'false')
        item.setArt({})

        logger.debug("-------------HANDLE-------------")
        logger.debug(handle)
        self.play(link, item)

    def set_ani_storage(self, ani_storage):
        self.ani_storage = ani_storage
        self.anilist_scrobbled = not self.does_it_require_update()


    def get_watched_percent(self, offset=None):
        if (self.getTotalTime() == 0):
            return 0
        else:
            return int((self.getTime() / (self.getTotalTime())) * 100)

    def scrobble_anilist(self):
        if (self.anilist_scrobbled):
            return
        if self.get_watched_percent() > 75:
            # Make update call
            # resp = update_anime()
            pass

    def does_it_require_update(self):
        # if int(self.ani_storage['current']['progress']) < int(self.ani_storage['current']['episode']):
        if 0:
            return True
        else:
            return False
