# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib.utils import kodiutils
from resources.lib.utils import kodilogging
from resources.lib.gogoanime1.gogoanime1 import get_mp4_for_conan, get_mp4, get_latest_episode_number
from resources.lib.kitsu.kitsu import get_token, get_trending_anime, get_popular_anime, get_anime_episodes, get_anime_by_id
from xbmcgui import ListItem, DialogProgress, Dialog
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from xbmc import Player, sleep


# TODO: Clean comments
# TODO: Debug log

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()

baseURL = "https://www.gogoanime1.com/watch/detective-conan/episode/episode-707"

@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(
        show_conan), ListItem("Detective Conan"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        trending_kitsu), ListItem("Trending Anime"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        popular_kitsu), ListItem("Popular Anime"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        test_kitsu), ListItem("Test Kitsu"), True)
    endOfDirectory(plugin.handle)

@plugin.route('/kitsu')
def test_kitsu():
    # get_token()
    # get_trending_anime()
    print("---popular----")
    # get_popular_anime()
    get_latest_episode_number("one-piece")

@plugin.route('/popular-anime')
def popular_kitsu():
    popular = get_popular_anime()
    create_anime_list(popular)

@plugin.route('/trending-anime')
def trending_kitsu():
    trending = get_trending_anime()
    create_anime_list(trending)

@plugin.route('/anime/<id>/<slug>/episodes/latest-<latest_episode>/<offset>')
def show_episodes(id, slug, latest_episode = -1, offset = 0):
    # Fix episode count a bit: says 1-20 but includes 1-21
    episodes = get_anime_episodes(id, offset)
    for episode in episodes:
        title = episode.canonicalTitle if episode.canonicalTitle != None else ""
        if (int(episode.number > int(latest_episode)) and int(latest_episode) != -1):
            item_label = ("Episode " + str(episode.number) +"[CR]" + "Not released yet" )
        else:
            item_label = ("Episode " + str(episode.number) +"[CR]" + title )
            
        list_item = ListItem(label = item_label)
        list_item.setInfo('video', episode.getEpisodeInfo())
        list_item.setArt(episode.getEpisodeArt())
        is_folder = False
        addDirectoryItem(plugin.handle, plugin.url_for(
            get_sources, slug, episode.number), list_item, is_folder)
    endOfDirectory(plugin.handle)

@plugin.route('/anime/<id>/<slug>/episodes-grouped')
def show_grouped_episodes(id, slug):
    # Need to find the exact number of released episodes
    # Kitsu adds dummy-empty unreleased episodes in long running shows
    # Until we find a new way to get that from an API we will use gogoanime1
    latest_episode = get_latest_episode_number(slug)
    anime = get_anime_by_id(id)
    # Create a list item per 20 episodes
    for start in range(1, int(latest_episode), 20):
        # print("In loop: " + str(start))
        end = str(int(start) + 19) if (int(start) + 19 <= int(latest_episode)) else str(latest_episode)
        list_item = ListItem(label=('Episodes ' + str(start) + '-' + str(end)).encode('utf-8'))
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = True
        addDirectoryItem(plugin.handle, plugin.url_for(
            show_episodes, id = id, slug = slug, offset=str(start), latest_episode=str(latest_episode)), list_item, is_folder)
    endOfDirectory(plugin.handle)
    pass

@plugin.route('/anime/<slug>/episode/<number>/sources')
def get_sources(slug, number):
    print("-------------get_sources-------------")
    progress = DialogProgress()
    progress.create("Getting sources", "getting les sources")
    urls_gogoanime = get_mp4(slug, number)
    progress.close()
    dialog = Dialog()
    url_index = dialog.select('Choose a source', ['GoGoAnime1 #1', 'GoGoAnime1 #2', 'GoGoAnime1 #3', 'GoGoAnime1 #4'])
    play_item = ListItem(path=urls_gogoanime[url_index])
    play_item.setProperty('mimetype', 'video/mp4')
    # Pass the item to the Kodi player.
    # setResolvedUrl(plugin.handle, True, listitem=play_item)
    print(urls_gogoanime)
    Player().play(urls_gogoanime[url_index] + "|User-Agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36&Referer=" + urls_gogoanime[url_index], play_item)

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

def create_anime_list(anime_list):
    for anime in anime_list:
        list_item = ListItem(label=anime.canonicalTitle)
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = True
        if (anime.episodeCount != None) and (anime.episodeCount < 80):
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_episodes, id = anime.id, slug = anime.slug, latest_episode = -1, offset = 0), list_item, is_folder)
        else:
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_grouped_episodes, id = anime.id, slug = anime.slug), list_item, is_folder)
    endOfDirectory(plugin.handle)

def run():
    plugin.run()
