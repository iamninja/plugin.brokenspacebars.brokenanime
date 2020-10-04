# -*- coding: utf-8 -*-

import logging

import routing
import xbmcaddon
from xbmcgui import ListItem, DialogProgress, Dialog
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from xbmc import Player, sleep

from resources.lib.utils.textformat import color_label
from resources.lib.utils.wrappers import Progress
from resources.lib.utils import kodiutils
from resources.lib.utils import kodilogging
from resources.lib.utils.settings import Settings
from resources.lib.memory.memory import MemoryStorage
from resources.lib.gogoanime1.gogoanime1 import get_mp4_for_conan, get_mp4, get_latest_episode_number
from resources.lib.kitsu.kitsu import get_slug
from resources.lib.anilist.anilist import get_latest_episode_info, get_anilist_user_library, get_anilist_anime, set_text_activity, update_anime, search_anime
from resources.lib.models.anime import Anime
from resources.lib.models.search import AnimeResults


# TODO: Clean comments

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()
settings = Settings()
baseURL = "https://www.gogoanime1.com/watch/detective-conan/episode/episode-707"

@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(
        anilist_user_library), ListItem("AniList - User Library"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        search), ListItem("Search Anime"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        test_kitsu), ListItem("Test"), True)
    if not settings.have_anilist_token():
        addDirectoryItem(plugin.handle, plugin.url_for(
            get_anilist_token), ListItem("Get AniList token"), True)
    endOfDirectory(plugin.handle)

@plugin.route('/test')
def test_kitsu():
    logger.debug("-----------Test-----------")
    search_results = search_anime('black', True)
    animeResults = AnimeResults(search_results['data']['Page'])
    logger.debug(animeResults.total)
    logger.debug(animeResults.list[0].title['romaji'])


@plugin.route('/get-anilist-token')
def get_anilist_token():
    dialog = Dialog()
    ok = dialog.yesno("Autheniticate AniList",
        '''
            1. Visit https://iamninja.github.io/plugin.brokenspacebars.brokenanime
            2. Click the button and authenticate into AniList
            3. Copy the access token and paste it on the next dialog''', nolabel="Back", yeslabel="Next"
    )
    if ok:
        token = dialog.input("Paste the token")
        logger.debug("Given token is: " + token)
        settings.set_anilistToken(token)
        logger.debug("Token in settings is: " + settings.get_anilistToken())
    else:
        pass

@plugin.route('/anilist-watching')
def anilist_user_library():
    entries = get_anilist_user_library(kodiutils.get_setting('usernameAnilist'))
    animeList = []
    for entry in entries:
        animeList.append(Anime(entry, "anilist"))
    for anime in animeList:
        logger.debug(anime.titles['romaji'].encode('utf-8'))
        list_item = ListItem(label=anime.canonicalTitle)
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = True
        if (anime.episodeCount != None) and (anime.episodeCount < 80):
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_episodes_anilist, in_list=1, id=anime.id, latest_episode=anime.episodeCount, offset=1), list_item, is_folder)
        else:
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_grouped_episodes_anilist, in_list=1, id=anime.id, latest_episode=anime.nextEpisode), list_item, is_folder)
    endOfDirectory(plugin.handle)

@plugin.route('/search')
def search():
    # Search through anilist
    # Open a text dialog (Dialog().input(...))
    dialog = Dialog()
    query = dialog.input("Enter search query")
    logger.debug("Search for: " + str(query))
    search_result = search_anime(query, True)
    animeResults = AnimeResults(search_result['data']['Page'])
    for anime in animeResults.list:
        list_item = ListItem(label=anime.title['userPreferred'])
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt)
        is_folder = True
        if anime.mediaListEntryId != None:
            in_list = 1
        addDirectoryItem(plugin.handle, plugin.url_for(
            show_episodes_anilist,
            in_list=in_list,
            id=anime.mediaListEntryId if in_list else anime.id,
            latest_episode=-1, offset=1), list_item, is_folder)
    endOfDirectory(plugin.handle)

# TODO: Needs refacotring
@plugin.route('/anime/anilist/<in_list>/<id>/episodes/latest-<latest_episode>/offset-<offset>')
def show_episodes_anilist(in_list, id, latest_episode = -1, offset = 1):
    anime = Anime(get_anilist_anime(id, in_list), "anilist")
    # logger.debug(anime)
    anime.slug = get_slug(anime.titles['romaji'].encode('utf-8'))
    # logger.debug(anime.slug)

    if anime.episodeCount != None:
        last = anime.episodeCount
    elif (int(latest_episode) - int(offset) <= 20):
        last = anime.nextEpisode
    else:
        last = int(offset) + 20 - 1

    for i in range(int(offset), last + 1):
        list_item = ListItem()
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = False
        if (i == anime.nextEpisode and anime.status == "RELEASING"):
            label = "Episode " + str(i) + "[CR]Airing after: " + anime.nextAiringAfter()
            if (i == anime.progress + 1):
                label = "(Up Next) " + label
            item_label = (color_label(label, 'green'))
            list_item.setLabel(item_label)
            addDirectoryItem(plugin.handle, "", list_item, False)
            break
        else:
            item_label = ("Episode " + str(i))
            if (i == anime.progress + 1):
                item_label = "(Up Next) " + item_label
                item_label = (color_label(item_label, 'blue'))
            list_item.setLabel(item_label)
            addDirectoryItem(plugin.handle, plugin.url_for(
                get_sources, anime.slug, i), list_item, is_folder)

    storage = MemoryStorage('ani')
    current = {
        'anime_id': anime.id,
        'progress': anime.progress,
        'requireCheck': True

    }
    storage['current'] = current
    endOfDirectory(plugin.handle)

@plugin.route('/anime/anilist/<in_list>/<id>/<latest_episode>/episodes-grouped')
def show_grouped_episodes_anilist(id, latest_episode, in_list):
    anime = Anime(get_anilist_anime(id, in_list), service = "anilist")
    if anime.nextEpisode != -1:
        latest_episode = anime.nextEpisode
    else:
        latest_episode = anime.episodeCount

    # Retrieve kitsu-anime object so we can get the titles (Deprecate it)
    # results = search_anime_kitsu(anime.titles['romaji'].encode('utf-8'))
    # anime = results[0]

    # Get slug from kitsu
    # anime.slug = get_slug(anime.titles['romaji'].encode('utf-8'))

    # Create a list item per 20 episodes
    for start in range(1, int(latest_episode), 20):
        # print("In loop: " + str(start))
        end = str(int(start) + 19) if (int(start) + 19 <= int(latest_episode)) else str(latest_episode)
        list_item = ListItem(label=('Episodes ' + str(start) + '-' + str(end)).encode('utf-8'))
        if anime.progress in range(int(start), int(end)):
            list_item.setLabel(color_label(list_item.getLabel(), 'blue'))
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = True
        addDirectoryItem(plugin.handle, plugin.url_for(
            # show_episodes, id = anime.id, slug = anime.slug, offset=str(start - 1), latest_episode=str(latest_episode)), list_item, is_folder)
            show_episodes_anilist, id = anime.id, offset=str(start), latest_episode=str(latest_episode)), list_item, is_folder)
    endOfDirectory(plugin.handle)
    pass

@plugin.route('/anime/<slug>/episode/<number>/sources')
def get_sources(slug, number):
    logger.debug("-------------get_sources-------------")
    progress = DialogProgress()
    progress.create("Getting sources", "getting les sources")
    slug = get_slug(slug)
    urls_gogoanime = get_mp4(slug, number)
    progress.close()
    dialog = Dialog()
    if urls_gogoanime != None:
        url_index = dialog.select('Choose a source', ['GoGoAnime1 #1'])
        play_item = ListItem(path=urls_gogoanime[url_index])
        play_item.setProperty('mimetype', 'video/mp4')
        Player().play(urls_gogoanime[url_index], play_item)
    else:
        url_index = dialog.select('Choose a source', ['Couldn\'t find sources'])
        play_item = ListItem(path="")
        play_item.setProperty('mimetype', 'video/mp4')
        Player().play("", play_item)
    # Add selected episode number to MemoryStorage
    storage = MemoryStorage('ani')
    current = storage['current']
    current['episode'] = int(number)
    current['requireCheck'] = True
    storage['current'] = current
    # Pass the item to the Kodi player.
    # setResolvedUrl(plugin.handle, True, listitem=play_item)
    # print(urls_gogoanime)
    # Player().play(urls_gogoanime[url_index], play_item)

def run():
    plugin.run()
