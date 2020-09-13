# -*- coding: utf-8 -*-

import requests
import json
import logging
from resources.lib.anilist.queries import queryForNextEpisode, queryForWatchingAnime, queryForAnimeInList
from resources.lib.anilist.mutations import mutationForSaveTextActivity, mutationForUpdatingAnime
from resources.lib.anilist.models import LatestEpisodeInfo
from resources.lib.utils.settings import Settings

baseURL = "https://graphql.anilist.co"
settings = Settings()
logger = logging.getLogger('plugin.brokenspacebars.brokenanime')

def make_request(query, variables, auth=False):
    logger.debug("-----Making post request to anilist.co-----")
    headers = {
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }
    if auth != False:
        headers['Authorization'] = 'Bearer ' + settings.get_anilistToken()

    resp = requests.post(baseURL, json={
        'query': query,
        'variables': variables
    }, headers=headers)
    resp.encoding = resp.apparent_encoding
    logger.debug("Response status: " + resp.status_code)
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
    return resp['data']['MediaListCollection']['lists'][0]['entries']

def get_anilist_anime(id):
    variables = {
        'id': id
    }
    resp = make_request(queryForAnimeInList, variables)
    return resp['data']['MediaList']

def set_text_activity(text):
    variables = {
        'text': text
    }
    resp = make_request(mutationForSaveTextActivity, variables, auth=True)
    return resp

# TODO: Maybe multi dispatch update_anime (id, entryId)

def update_anime(id, newProgress):
    variables = {
        'id': id,
        'newProgress': newProgress
    }
    resp = make_request(mutationForUpdatingAnime, variables, auth=True)
    return resp
