# -*- coding: utf-8 -*-

class Episode():
    def __init__(self, response_dict):
        self.id = response_dict['id']
        # ISO 8601 e.g. 2013-02-20T18:20:39.003Z
        self.createdAt = response_dict['attributes']['createdAt']
        # ISO 8601 e.g. 2013-02-20T18:20:39.003Z
        self.updatedAt = response_dict['attributes']['updatedAt']
        self.synopsis = response_dict['attributes']['synopsis']
        # object
        self.titles = response_dict['attributes']['titles']
        self.canonicalTitle = response_dict['attributes']['canonicalTitle']
        self.seasonNumber = response_dict['attributes']['seasonNumber']
        self.number = response_dict['attributes']['number']
        self.relativeNumber = response_dict['attributes']['relativeNumber']
        # YYYY-MM-DD
        self.airdate = response_dict['attributes']['airdate']
        self.length = response_dict['attributes']['length']
        # object
        self.thumbnail = response_dict['attributes']['thumbnail']

    def getEpisodeInfo(self):
        return {
            'plot': self.synopsis,
            'title': self.canonicalTitle,
            'duration': self.length,
            'premiered': self.airdate,
            'season': self.seasonNumber,
            'episode': self.number,
            'mediatype': "episode",
        }

    def getEpisodeArt(self):
        thumb = ""
        if self.thumbnail != None:
            thumb = self.thumbnail['original']
        return {
            'thumb': thumb
        }

class Episodes():
    def __init__(self, response_dict):
        self.episode = []
        for episode in response_dict['data']:
            self.episode.append(Episode(episode))
        self.count = response_dict['meta']['count']
