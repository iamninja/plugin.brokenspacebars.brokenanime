# -*- coding: utf-8 -*-

import logging

import routing
import xbmcaddon
import requests

from xbmcgui import ListItem, DialogProgress, Dialog
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from xbmc import sleep

from resources.lib.brokenxbmc.brokenplayer import BrokenPlayer
from resources.lib.utils.textformat import color_label
from resources.lib.utils.wrappers import Progress
from resources.lib.utils import kodiutils
from resources.lib.utils import kodilogging
from resources.lib.utils.settings import Settings
from resources.lib.memory.memory import MemoryStorage
from resources.lib.gogoanime1.gogoanime1 import get_mp4_for_conan, get_mp4, get_latest_episode_number
from resources.lib.kitsu.kitsu import get_slug
from resources.lib.anilist.anilist import get_latest_episode_info, get_anilist_user_library, get_anilist_anime, \
    set_text_activity, update_anime, search_anime
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
    # search_results = search_anime('black', True)
    # animeResults = AnimeResults(search_results['data']['Page'])
    # logger.debug(animeResults.total)
    # logger.debug(animeResults.list[0].title['romaji'])
    logger.debug(plugin.handle)
    base_url = "https://api.real-debrid.com/rest/1.0/"

    data = '''
        Authorization: Bearer NJDTPTQ2ZV6VCG6AJPA5QXLLJOSJDSMBIM5RSBGBUWONUUGTZXKA
    '''
    headers = {
        'Authorization': 'Bearer NJDTPTQ2ZV6VCG6AJPA5QXLLJOSJDSMBIM5RSBGBUWONUUGTZXKA'
    }
    requests.get(base_url + "user", headers=headers)
    resp = requests.post(base_url + "torrents/addMagnet", 
        headers=headers,
        data = {'magnet': 'magnet:?xt=urn:btih:b53e5ddf17f3f4da673925a0c64d9a738619d238&dn=%5BSubsPlease%5D%20Kimetsu%20no%20Yaiba%20-%20Yuukaku-hen%20-%2004%20%281080p%29%20%5B16EAAF6C%5D.mkv&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce'})
    details = resp.json()
    select = requests.post(base_url + "torrents/selectFiles/" + details['id'],
        headers = headers,
        data = {'files': '1'})
    info = requests.get(base_url + "torrents/info/" + details['id'], headers = headers).json()
    links = requests.post(base_url + "unrestrict/link",
        headers=headers,
        data = {'link': info['links'][0]}).json()
    player = BrokenPlayer()
    player.play(links['download'])

@plugin.route('/get-anilist-token')
def get_anilist_token():
    dialog = Dialog()
    ok = dialog.yesno("Authenticate AniList",
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
        logger.debug(anime.titles['romaji'])
        list_item = ListItem(label=anime.canonicalTitle)
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = True
        if (anime.episodeCount is not None) and (anime.episodeCount < 80):
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_episodes_anilist, in_list=1, id=anime.id, latest_episode=anime.episodeCount, offset=1), list_item,
                             is_folder)
        else:
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_grouped_episodes_anilist, in_list=1, id=anime.id, latest_episode=anime.nextEpisode), list_item,
                             is_folder)
    endOfDirectory(plugin.handle)


# TODO Not working
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
        if anime.mediaListEntryId is not None:
            in_list = 1
        addDirectoryItem(plugin.handle, plugin.url_for(
            show_episodes_anilist,
            in_list=in_list,
            id=anime.mediaListEntryId if in_list else anime.id,
            latest_episode=-1, offset=1), list_item, is_folder)
    endOfDirectory(plugin.handle)


# TODO: Needs refacotring
@plugin.route('/anime/anilist/<in_list>/<id>/episodes/latest-<latest_episode>/offset-<offset>')
def show_episodes_anilist(in_list, id, latest_episode=-1, offset=1):
    anime = Anime(get_anilist_anime(id, in_list), "anilist")
    # logger.debug(anime)
    anime.slug = get_slug(anime.titles['romaji'])
    # logger.debug(anime.slug)

    if anime.episodeCount is not None:
        last = anime.episodeCount
    elif int(latest_episode) - int(offset) <= 20:
        last = anime.nextEpisode
    else:
        last = int(offset) + 20 - 1

    for i in range(int(offset), last + 1):
        list_item = ListItem()
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = False
        if i == anime.nextEpisode and anime.status == "RELEASING":
            label = "Episode " + str(i) + "[CR]Airing after: " + anime.nextAiringAfter()
            if i == anime.progress + 1:
                label = "(Up Next) " + label
            item_label = (color_label(label, 'green'))
            list_item.setLabel(item_label)
            addDirectoryItem(plugin.handle, "", list_item, False)
            break
        else:
            item_label = ("Episode " + str(i))
            if i == anime.progress + 1:
                item_label = "(Up Next) " + item_label
                item_label = (color_label(item_label, 'blue'))
            list_item.setLabel(item_label)
            addDirectoryItem(plugin.handle, plugin.url_for(
                get_sources, plugin.handle, anime.slug, i), list_item, is_folder)

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
    anime = Anime(get_anilist_anime(id, in_list), service="anilist")
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
        list_item = ListItem(label=('Episodes ' + str(start) + '-' + str(end)))
        if anime.progress in range(int(start), int(end)):
            list_item.setLabel(color_label(list_item.getLabel(), 'blue'))
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = True
        addDirectoryItem(plugin.handle, plugin.url_for(
            # show_episodes, id = anime.id, slug = anime.slug, offset=str(start - 1), latest_episode=str(
            # latest_episode)), list_item, is_folder)
            show_episodes_anilist, id=anime.id, offset=str(start), latest_episode=str(latest_episode)), list_item,
                         is_folder)
    endOfDirectory(plugin.handle)
    pass


@plugin.route('/<handle>/anime/<slug>/episode/<number>/sources')
def get_sources(handle, slug, number):
    logger.debug("-------------get_sources-------------")
    progress = DialogProgress()
    progress.create("Getting sources", "getting les sources")
    slug = get_slug(slug)
    urls_gogoanime = get_mp4(slug, number)
    progress.close()
    dialog = Dialog()
    player = BrokenPlayer()
    if urls_gogoanime is not None:
        url_index = dialog.select('Choose a source', ['GoGoAnime1 #1'])
        play_item = ListItem(path=urls_gogoanime[url_index])
        play_item.setProperty('mimetype', 'video/mp4')
        print("---------------------Starting BrokenPlayer")
        # player = BrokenPlayer()
        player.play(urls_gogoanime[url_index], play_item)
        # player.play_source(urls_gogoanime[url_index], handle, args={})
    else:
        url_index = dialog.select('Choose a source', ['Couldn\'t find sources'])
        play_item = ListItem(path="")
        play_item.setProperty('mimetype', 'video/mp4')
        BrokenPlayer().play("", play_item)
        pass

    # Add selected episode number to MemoryStorage
    storage = MemoryStorage('ani')
    current = storage['current']
    current['episode'] = int(number)
    current['requireCheck'] = True
    storage['current'] = current

    player.set_ani_storage(current)
    sleep(500)  # Wait until playback starts
    while player.isPlaying():
        logger.debug("aaaloooping")
        logger.debug(player.get_watched_percent())
        sleep(500)

    # Pass the item to the Kodi player.
    # setResolvedUrl(plugin.handle, True, listitem=play_item)
    # print(urls_gogoanime)
    # Player().play(urls_gogoanime[url_index], play_item)


def run():
    plugin.run()
