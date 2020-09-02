# -*- coding: utf-8 -*-

import requests
import json
from resources.lib.anilist.queries import queryForNextEpisode, queryForWatchingAnime, queryForAnimeInList
from resources.lib.anilist.models import LatestEpisodeInfo

baseURL = "https://graphql.anilist.co"

def make_request(query, variables, auth = False):
    print("-----Making post request to anilist.co-----")
    headers = {
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }
    if auth != False:
        headers['Authorization'] = 'Bearer ' + 't0k3n'

    resp = requests.post(baseURL, json = {
        'query': query,
        'variables': variables
    }, headers = headers)
    resp.encoding = resp.apparent_encoding
    return json.loads(resp.text)

def get_latest_episode_info(slug):
    variables = {
        'queryString': slug,
    }
    resp = make_request(queryForNextEpisode, variables)
    latestInfo = LatestEpisodeInfo(resp)
    return latestInfo

def get_anilist_user_library(userName):
    variables = {
        'userName': userName
    }
    resp = make_request(queryForWatchingAnime, variables)
    # print(resp)
    return resp['data']['MediaListCollection']['lists'][0]['entries']

def get_anilist_anime(id):
    variables = {
        'id': id
    }
    resp = make_request(queryForAnimeInList, variables)
    return resp['data']['MediaList']
