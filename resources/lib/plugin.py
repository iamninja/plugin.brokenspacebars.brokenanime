# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib.utils import kodiutils
from resources.lib.utils import kodilogging
from resources.lib.gogoanime1.gogoanime1 import get_mp4_for_conan
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()

baseURL = "https://www.gogoanime1.com/watch/detective-conan/episode/episode-707"

@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(
        show_conan), ListItem("Detective Conan"), True)
    endOfDirectory(plugin.handle)


@plugin.route('/conan')
def show_conan():
    for i in range(700, 900, 10):
        list_item = ListItem(label=("Detective Conan: " + str(i + 1) + " - " + str(i + 10)))
        # list_item.setLabel2(movie.expiration_date)
        # list_item.setInfo('video', movie.getMovieInfo())
        # list_item.setArt(movie.getMovieArt())
        list_item.setProperty('IsPlayable', 'False')
        # url = get_mp4_from_url(baseURL)
        is_folder = True
        addDirectoryItem(plugin.handle, plugin.url_for(
            show_conan_episodes, i + 1), list_item, is_folder)
    endOfDirectory(plugin.handle)

@plugin.route('/conan/<episodes>')
def show_conan_episodes(episodes):
    for i in range(int(episodes), int(episodes) + 10):
        list_item = ListItem(
            label=("Detective Conan - " + str(i)), 
            offscreen=True)
        # list_item.setLabel2(movie.expiration_date)
        # list_item.setInfo('video', movie.getMovieInfo())
        # list_item.setArt(movie.getMovieArt())
        list_item.setProperty('IsPlayable', 'False')
        # url = get_mp4_for_conan(i)
        is_folder = True
        list_item
        addDirectoryItem(
            plugin.handle, 
            plugin.url_for(play_conan, str(i)), 
            list_item, is_folder)
    endOfDirectory(plugin.handle)

@plugin.route('/conan/play/<episode>')
def play_conan(episode):
    item = ListItem(label=("Play episode"))
    item.setProperty('IsPlayable', 'True')
    is_folder = False
    addDirectoryItem(
            plugin.handle, 
            get_mp4_for_conan(episode),
            item, is_folder)
    endOfDirectory(plugin.handle)

def run():
    plugin.run()
