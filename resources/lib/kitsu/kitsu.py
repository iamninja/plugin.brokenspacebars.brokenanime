# -*- coding: utf-8 -*-

import requests
import json
import pickle
from xbmcaddon import Addon
from resources.lib.utils.wrappers import Progress
from resources.lib.kitsu.models.anime import Anime
from resources.lib.kitsu.models.episode import Episode
from resources.lib.kitsu.models.libraryentries import Library, LibraryEntry

CLIENT_ID = "dd031b32d2f56c990b1425efe6c42ad847e7fe3ab46bf1299f05ecd856bdb7dd"
CLIENT_SECRET = "54d7307928f63414defd96399fc31ba847961ceaecef3a5fd93144e960c0e151"
tokenURL = "https://kitsu.io/api/oauth/token"
baseURL =  "https://kitsu.io/api/edge/"

addon = Addon('plugin.brokenspacebars.brokenanime')

# TODO: save pickles in a better place
# TODO: Clean comments
# TODO: Debug log

def get_token():
    addon = Addon('plugin.brokenspacebars.brokenanime')
    data = {
        'grant_type': 'password',
        'username': addon.getSetting('username'),
        'password': addon.getSetting('password'),
    }
    # print(data)
    resp = requests.post(tokenURL, data)
    print(addon.getAddonInfo('profile'))
    # print(resp.text)
    if resp.status_code == 200:
        pickle.dump(json.loads(resp.text), open(
            addon.getAddonInfo('path') + "/kitsu.pickle", "wb"))
        # with open(addon.getAddonInfo('path') + 'kitsu.json', 'w') as outfile:
        #     json.dump(resp.text, outfile)
    else:
        print("Couldn't get response")
    check_token()
    

def refresh_token(ref_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': ref_token
    }
    resp = requests.post(tokenURL, data)
    print(resp)
    if resp.status_code == 200:
        pickle.dump(json.loads(resp.text), open(
            addon.getAddonInfo('path') + "/kitsu.pickle", "wb"))
    else:
        print("Couldn't get response")

# TODO: Check expiration
def check_token():
    addon = Addon('plugin.brokenspacebars.brokenanime')
    data = pickle.load(open(
        addon.getAddonInfo('path') + "/kitsu.pickle", "rb"))
    # data = {}
    # with open(addon.getAddonInfo('profile') + "kitsu.json", "r") as json_file:
    #     data = json.load(json_file)
    return data['access_token']

def get_trending_anime():
    resp = requests.get(baseURL + 'trending/anime')
    data = json.loads(resp.text)
    trending_anime = []
    # print(data)
    for anime in data['data']:
        trending_anime.append(Anime(anime))
    for anime in trending_anime:
        print(anime.slug)
    return trending_anime

def get_popular_anime():
    resp = requests.get(baseURL + 'anime?sort=ratingRank&page[limit]=20&page[offset]=0')
    data = json.loads(resp.text)
    popular_anime = []
    for anime in data['data']:
        popular_anime.append(Anime(anime))
    # print(data)
    for anime in popular_anime:
        print(anime.slug)
    return popular_anime

def get_user_id(progress):
    progress.update(0, "Retrieving user data")
    resp = requests.get(baseURL + 'users?filter[name]=' + addon.getSetting('username'))
    data = json.loads(resp.text)
    return data['data'][0]['id']

def get_user_library(progress):
    userId = get_user_id(progress)
    resp = requests.get(baseURL + 'library-entries?filter[userId]=' + userId + '&filter[kind]=anime&filter[status]=current&page[limit]=20&page[offset]=0')
    data = json.loads(resp.text)
    library = Library(data['meta'])
    progress.max = library.count + 1
    for entry in data['data']:
        progress.easyUpdate()
        library.entries.append(LibraryEntry(entry))
    while ('next' in data['links'].keys()):
        resp = requests.get(data['links']['next'])
        data = json.loads(resp.text)
        for entry in data['data']:
            progress.easyUpdate()
            library.entries.append(LibraryEntry(entry))
    return progress, library


def get_anime_episodes(id, offset):
    resp = requests.get(baseURL + 'anime/' + str(id) + '/episodes?page[limit]=20&page[offset]=' + str(offset))
    data = json.loads(resp.text)
    episodes = []
    for episode in data['data']:
        episodes.append(Episode(episode))
    if str(offset) != '0':
        return episodes
    while ('next' in data['links'].keys()):
        resp = requests.get(data['links']['next'])
        data = json.loads(resp.text)
        for episode in data['data']:
            episodes.append(Episode(episode))
    print(episodes[1].canonicalTitle)
    return episodes

def search_anime(query):
    resp = requests.get(baseURL + 'anime?filter[text]=' + str(query))
    data = json.loads(resp.text)
    search_results = []
    for anime in data['data']:
        search_results.append(Anime(anime))
    # for anime in search_results:
    #     print(anime.slug)
    return search_results

def get_anime_by_id(id):
    resp = requests.get(baseURL + 'anime/' + str(id))
    data = json.loads(resp.text)
    anime = Anime(data['data'])
    return anime