# -*- coding: utf-8 -*-

import requests
import json
from resources.lib.kitsu.models.anime import Anime

baseURL =  "https://kitsu.io/api/edge/"

class LibraryEntry:
    
    def __init__(self, data):
        self.id = data['id']
        self.createdAt = data['attributes']['createdAt']
        self.updatedAt = data['attributes']['updatedAt']
        self.status = data['attributes']['status']
        self.progress = data['attributes']['progress']
        self.volumesOwned = data['attributes']['volumesOwned']
        self.reconsuming = data['attributes']['reconsuming']
        self.reconsumeCount = data['attributes']['reconsumeCount']
        self.notes = data['attributes']['notes']
        self.private = data['attributes']['private']
        self.reactionSkipped = data['attributes']['reactionSkipped']
        self.progressedAt = data['attributes']['progressedAt']
        self.startedAt = data['attributes']['startedAt']
        self.finishedAt = data['attributes']['finishedAt']
        self.rating = data['attributes']['rating']
        self.ratingTwenty = data['attributes']['ratingTwenty']

        self.animeLink = data['relationships']['anime']['links']['related']

        # Here will be stored the Anime object
        self.anime = self.__getAnime()
    
    def __getAnime(self):
        resp = requests.get(self.animeLink)
        data = json.loads(resp.text)
        anime = Anime(data['data'])
        return anime


class Library:

    def __init__(self, meta):
        self.current = meta['statusCounts']['current']
        self.completed = meta['statusCounts']['completed']
        self.onHold = meta['statusCounts']['onHold']
        self.planned = meta['statusCounts']['planned']
        self.count = meta['count']

        # Here will be stored LibraryEntry objects
        self.entries = []