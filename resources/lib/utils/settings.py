# -*- coding: utf-8 -*-

import os
import json
import logging

import xbmcaddon
from xbmc import translatePath

from resources.lib.utils import kodilogging

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()

class Settings():

    def __init__(self):
        self.__addon = xbmcaddon.Addon()
        self.__profile = translatePath(self.__addon.getAddonInfo('profile')).decode('utf-8')
        if self.settings_file_exists():
            self.load_settings()
        else:
            logger.debug("3 - " + self.__addon.getSetting('usernameKitsu'))
            self.__kitsuUsername = self.__addon.getSetting('usernameKitsu')
            self.__kitsuPassword = self.__addon.getSetting('passwordKitsu')
            self.__anilistUsername = self.__addon.getSetting('usernameAnilist')
            self.__anilistToken = ""
            self.save_settings()


    def settings_file_exists(self):
        if os.path.isfile(self.__profile + '/settings.json'):
            return True
        else:
            return False

    def load_settings(self):
        with open(self.__profile + '/settings.json') as file:
            data = json.load(file)
            self.__kitsuUsername = data['kitsu']['username']
            self.__kitsuPassword = data['kitsu']['password']
            self.__anilistUsername = data['anilist']['username']
            self.__anilistToken = data['anilist']['access_token']

    def save_settings(self):
        data = {
            'kitsu': { },
            'anilist': { }
        }
        data['kitsu']['username'] = self.__kitsuUsername
        data['kitsu']['password'] = self.__kitsuPassword
        data['anilist']['username'] = self.__anilistUsername
        data['anilist']['access_token'] = self.__anilistToken
        with open(self.__profile + '/settings.json', 'w') as file:
            json.dump(data, file)

    def have_anilist_token(self):
        if self.__anilistToken != "":
            return True
        else:
            return False

    def get_kitsuUsername(self):
        return self.__kitsuUsername

    def set_kitsuUsername(self, new_value):
        self.__kitsuUsername = new_value
        self.save_settings()

    def get_kitsuPassword(self):
        return self.__kitsuPassword

    def set_kitsuPassword(self, new_value):
        self.__kitsuPassword = new_value
        self.save_settings()

    def get_anilistUsername(self):
        return self.__anilistUsername

    def set_anilistUsername(self, new_value):
        self.__anilistUsername = new_value
        self.save_settings()

    def get_anilistToken(self):
        return self.__anilistToken

    def set_anilistToken(self, new_value):
        self.__anilistToken = new_value
        self.save_settings()

