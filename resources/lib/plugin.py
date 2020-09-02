# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from pprint import pprint
from resources.lib.utils.textformat import color_label
from resources.lib.utils.wrappers import Progress
from resources.lib.utils import kodiutils
from resources.lib.utils import kodilogging
from resources.lib.utils.settings import Settings
from resources.lib.gogoanime1.gogoanime1 import get_mp4_for_conan, get_mp4, get_latest_episode_number
from resources.lib.kitsu.kitsu import get_token, get_trending_anime, get_popular_anime, get_anime_episodes, get_anime_by_id, search_anime_kitsu, get_user_library, get_slug
from resources.lib.anilist.anilist import get_latest_episode_info, get_anilist_user_library, get_anilist_anime
from resources.lib.models.anime import Anime
from xbmcgui import ListItem, DialogProgress, Dialog
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from xbmc import Player, sleep


# TODO: Clean comments
# TODO: Debug log

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
        show_conan), ListItem("Detective Conan"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        show_grouped_episodes, id = 210, slug = "detective-conan"), ListItem("Detective Conan - Kitsu"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(
        test_kitsu), ListItem("Test"), True)
    if not settings.have_anilist_token():
        addDirectoryItem(plugin.handle, plugin.url_for(
            get_anilist_token), ListItem("Get AniList token"), True)
    endOfDirectory(plugin.handle)

@plugin.route('/test')
def test_kitsu():
    print("-----------Test-----------")
    # get_token()
    # get_trending_anime()
    # get_popular_anime()
    # get_latest_episode_number("one-piece")
    # search_anime("black clover")
    # get_latest_episode_info("black-clover")
    print("1 - " + ADDON.getSetting("usernameKitsu"))
    print("2 - " + kodiutils.get_setting('usernameAnilist'))
    print(settings.kitsuUsername)
    print(settings.kitsuPassword)

@plugin.route('/get_token')
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
        print(token)
    else:
        pass



@plugin.route('/anilist-watching')
def anilist_user_library():
    entries = get_anilist_user_library(kodiutils.get_setting('usernameAnilist'))
    animeList = []
    for entry in entries:
        animeList.append(Anime(entry, "anilist"))
    for anime in animeList:
        print(anime.titles['romaji'].encode('utf-8'))
        list_item = ListItem(label=anime.canonicalTitle)
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = True
        if (anime.episodeCount != None) and (anime.episodeCount < 80):
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_episodes_anilist, id = anime.id, latest_episode = anime.episodeCount), list_item, is_folder)
        else:
            addDirectoryItem(plugin.handle, plugin.url_for(
                show_grouped_episodes_anilist, id = anime.id, latest_episode = anime.nextEpisode), list_item, is_folder)
    endOfDirectory(plugin.handle)

@plugin.route('/search')
def search():
    # via kitsu for now
    # Open a text dialog (Dialog().input(...))
    dialog = Dialog()
    query = dialog.input("Enter search query")
    print("Search for: " + str(query))
    search_result = search_anime_kitsu(query)
    create_anime_list(search_result)

@plugin.route('/anime/anilist/<id>/episodes/latest-<latest_episode>')
def show_episodes_anilist(id, latest_episode = -1):
    anime = Anime(get_anilist_anime(id), "anilist")
    # print(anime)
    anime.slug = get_slug(anime.titles['romaji'].encode('utf-8'))
    # print(anime.slug)
    if anime.episodeCount != None:
        last = anime.episodeCount
    else:
        last = anime.nextEpisode
    for i in range(1, last + 1):
        list_item = ListItem()
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = False
        if (i == anime.nextEpisode and anime.status == "RELEASING"):
            label = "Episode " + str(i) + "[CR]Airing after: " + anime.nextAiringAfter()
            item_label = (color_label(label, 'green'))
            list_item.setLabel(item_label)
            addDirectoryItem(plugin.handle, "", list_item, False)
            break
        else:
            item_label = ("Episode " + str(i))
            list_item.setLabel(item_label)
            addDirectoryItem(plugin.handle, plugin.url_for(
                get_sources, anime.slug, i), list_item, is_folder)
    endOfDirectory(plugin.handle)

@plugin.route('/anime/anilist/<id>/<latest_episode>/episodes-grouped')
def show_grouped_episodes_anilist(id, latest_episode):
    anime = Anime(get_anilist_anime(id), service = "anilist")
    if anime.nextEpisode != -1:
        latest_episode = anime.nextEpisode
    else:
        latest_episode = anime.episodeCount
    results = search_anime_kitsu(anime.titles['romaji'].encode('utf-8'))
    anime = results[0]
    # anime.slug = get_slug(anime.titles['romaji'].encode('utf-8'))

    # Create a list item per 20 episodes
    for start in range(1, int(latest_episode), 20):
        # print("In loop: " + str(start))
        end = str(int(start) + 19) if (int(start) + 19 <= int(latest_episode)) else str(latest_episode)
        list_item = ListItem(label=('Episodes ' + str(start) + '-' + str(end)).encode('utf-8'))
        list_item.setInfo('video', anime.getAnimeInfo())
        list_item.setArt(anime.getAnimeArt())
        is_folder = True
        addDirectoryItem(plugin.handle, plugin.url_for(
            show_episodes, id = anime.id, slug = anime.slug, offset=str(start - 1), latest_episode=str(latest_episode)), list_item, is_folder)
    endOfDirectory(plugin.handle)
    pass

@plugin.route('/anime/<slug>/episode/<number>/sources')
def get_sources(slug, number):
    print("-------------get_sources-------------")
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
    # Pass the item to the Kodi player.
    # setResolvedUrl(plugin.handle, True, listitem=play_item)
    # print(urls_gogoanime)
    # Player().play(urls_gogoanime[url_index], play_item)

#For Conan
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

# For Conan
@plugin.route('/anime/kitsu/<id>/<slug>/episodes/latest-<latest_episode>/<offset>')
def show_episodes(id, slug, latest_episode = -1, offset = 0):
    # Kitsu will handle episodes so it can show the title
    # Fix episode count a bit: says 1-20 but includes 1-21
    episodes = get_anime_episodes(id, offset)
    for episode in episodes:
        title = episode.canonicalTitle if episode.canonicalTitle != None else ""
        if int(episode.number) == int(latest_episode):
            item_label = ("Episode " + str(episode.number) + "[CR]" + "Not released yet" )
        else:
            item_label = ("Episode " + str(episode.number) + "[CR]" + title )
        list_item = ListItem(label = item_label)
        list_item.setInfo('video', episode.getEpisodeInfo())
        list_item.setArt(episode.getEpisodeArt())
        is_folder = False
        addDirectoryItem(plugin.handle, plugin.url_for(
            get_sources, slug, episode.number), list_item, is_folder)
        if int(episode.number) == int(latest_episode):
            item_label = ("Episode " + str(episode.number) + "[CR]" + "Not released yet" )
            break
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
    item.setInfo('video',{
        'mediatype': "tvshow"
    })
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
