# -*- coding: utf-8 -*-

class Anime:
    def __init__(self, response_dict):
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
        self.subtype = response_dict['attributes']['subtype']
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
    
    def getAnimeInfo(self):
        return {
            'plot': self.synopsis,
            'title': self.canonicalTitle,
            'duration': self.episodeLength,
            'premiered': self.startDate,
            'status': self.status,
            'mediatype': "tvshow",
            'rating': self.averageRating,
            'trailer': "https://www.youtube.com/watch?v=" + str(self.youtubeVideoId)
        }

    def getAnimeArt(self):
        return {
            'fanart': self.posterImage['original'],
            'thumb': self.coverImage['original']
        }