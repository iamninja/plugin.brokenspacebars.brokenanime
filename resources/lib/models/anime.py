# -*- coding: utf-8 -*-

from time import time
from resources.lib.utils.textformat import secondsToRemaining, createSlug

# TODO: Get trailer from anilist query

class Anime:

    def __init__(self, response_dict, service = "kitsu"):
        self.service = service
        if service == "kitsu":
            self.__loadFromKitsu(response_dict)
        elif service == "anilist":
            self.__loadFromAnilist(response_dict)

    def getAnimeInfo(self):
        return {
            'plot': self.synopsis,
            'title': self.canonicalTitle,
            'duration': self.episodeLength,
            'premiered': self.startDate,
            'status': self.status,
            'mediatype': "tvshow",
            'rating': self.averageRating,
            'trailer': "https://www.youtube.com/watch?v=" + str(self.youtubeVideoId) if hasattr(self, 'youtubeVideoId') else ""
        }

    def getAnimeArt(self):
        thumb = ""
        posterImage = ""
        if self.coverImage != None:
            if self.service == "kitsu":
                posterImage = self.coverImage['original']
            elif self.service == "anilist":
                posterImage = self.coverImage
        if self.posterImage != None:
            if self.service == "kitsu":
                thumb = self.posterImage['original']
            elif self.service == "anilist":
                thumb = self.posterImage['large']
        return {
            'fanart': posterImage,
            'thumb': thumb
        }

    def __loadFromKitsu(self, response_dict):
        subtype = {
            "ONA": "ONA",
            "OVA": "OVA",
            "TV": "TV",
            "movie": "Movie",
            "music": "Music",
            "special": "Special"
        }
        self.id = response_dict['id']
        self.createdAt = response_dict['attributes']['createdAt']
        self.updatedAt = response_dict['attributes']['updatedAt']
        self.slug = response_dict['attributes']['slug']
        self.synopsis = response_dict['attributes']['synopsis']
        # object
        self.titles = response_dict['attributes']['titles']
        self.canonicalTitle = response_dict['attributes']['canonicalTitle']
        # array
        self.abbreviatedTitles = response_dict['attributes']['abbreviatedTitles']
        self.averageRating = response_dict['attributes']['averageRating']
        # object
        self.ratingFrequencies = response_dict['attributes']['ratingFrequencies']
        self.usercount = response_dict['attributes']['userCount']
        self.favoritesCount = response_dict['attributes']['favoritesCount']
        # YYYY-MM-DD
        self.startDate = response_dict['attributes']['startDate']
        # YYYY-MM-DD
        self.endDate = response_dict['attributes']['endDate']
        self.popularityRank = response_dict['attributes']['popularityRank']
        self.ratingRank = response_dict['attributes']['ratingRank']
        # enum
        # self.ageRating = response_dict['attributes']['ageRating']
        self.ageRatingGuide = response_dict['attributes']['ageRatingGuide']
        # enum
        self.subtype = subtype.get(response_dict['attributes']['subtype'])
        # enum
        self.status = response_dict['attributes']['status']
        self.tba = response_dict['attributes']['tba']
        # object
        self.posterImage = response_dict['attributes']['posterImage']
        # object
        self.coverImage = response_dict['attributes']['coverImage']
        self.episodeCount = response_dict['attributes']['episodeCount']
        self.episodeLength = response_dict['attributes']['episodeLength']
        self.youtubeVideoId = response_dict['attributes']['youtubeVideoId']
        # enum
        self.showType = response_dict['attributes']['showType']
        # boolean
        self.nsfw = False if response_dict['attributes']['nsfw'] == 'false' else True

    def __loadFromAnilist(self, response_dict):
        self.id = response_dict['id']
        self.progress = response_dict['progress'] if 'progress' in response_dict.keys() else 0
        # self.createdAt = response_dict['attributes']['createdAt']
        # self.updatedAt = response_dict['attributes']['updatedAt']
        # self.slug = response_dict['attributes']['slug']
        self.synopsis = response_dict['media']['description']
        # object
        self.titles = response_dict['media']['title']
        self.canonicalTitle = response_dict['media']['title']['userPreferred']
        # array
        self.abbreviatedTitles = response_dict['media']['synonyms']
        self.averageRating = response_dict['media']['averageScore']
        # YYYY-MM-DD
        self.startDate = self.__setDateAnilist(response_dict['media']['startDate'])
        # YYYY-MM-DD
        self.endDate = self.__setDateAnilist(response_dict['media']['endDate'])
        # enum
        self.subtype = response_dict['media']['type']
        # enum
        self.status = response_dict['media']['status']
        # self.tba = response_dict['media']['tba']
        # object
        self.posterImage = response_dict['media']['coverImage']
        # string
        self.coverImage = response_dict['media']['bannerImage']
        self.episodeCount = response_dict['media']['episodes']
        self.episodeLength = response_dict['media']['duration']
        # self.youtubeVideoId = response_dict['media']['youtubeVideoId']
        # enum
        # self.showType = response_dict['media']['showType']
        # boolean
        self.nsfw = False if response_dict['media']['isAdult'] == 'false' else True
        if response_dict['media']['nextAiringEpisode'] != None:
            self.nextEpisode = response_dict['media']['nextAiringEpisode']['episode']
            self.airingAt = response_dict['media']['nextAiringEpisode']['airingAt']
        else:
            self.nextEpisode = -1
            self.airingAt = None
        self.slug = createSlug(self.titles['romaji'])

    def __setDateAnilist(self, dict):
        return str(dict['year']) + "-" + str(dict['month']) + "-" + str(dict["day"])

    def nextAiringAfter(self):
        remainingSeconds = int(self.airingAt) - int(time())
        return secondsToRemaining(remainingSeconds)

    def nextAiringDate(self):
        pass
