# -*- coding: utf-8 -*-

import os
import json
import xbmcaddon
from xbmc import translatePath

class Settings():

    def __init__(self):
        self.__addon = xbmcaddon.Addon()
        self.__profile = translatePath(self.__addon.getAddonInfo('profile')).decode('utf-8')
        if self.settings_file_exists():
            self.load_settings()
        else:
            print("3 - " + self.__addon.getSetting('usernameKitsu'))
            self.kitsuUsername = self.__addon.getSetting('usernameKitsu')
            self.kitsuPassword = self.__addon.getSetting('passwordKitsu')
            self.anilistUsername = self.__addon.getSetting('usernameAnilist')
            self.anilistToken = ""
            self.save_settings()


    def settings_file_exists(self):
        if os.path.isfile(self.__profile + '/settings.json'):
            True
        else:
            False

    def load_settings(self):
        with open(self.__profile + '/settings.json') as file:
            data = json.load(file)
            self.kitsuUsername = data['kitsu']['username']
            self.kitsuPassword = data['kitsu']['password']
            self.anilistUsername = data['anilist']['username']
            self.anilistToken = data['anilist']['access_token']

    def save_settings(self):
        data = {
            'kitsu': { },
            'anilist': { }
        }
        data['kitsu']['username'] = self.kitsuUsername
        data['kitsu']['password'] = self.kitsuPassword
        data['anilist']['username'] = self.anilistUsername
        data['anilist']['access_token'] = self.anilistToken
        with open(self.__profile + '/settings.json', 'w') as file:
            json.dump(data, file)
