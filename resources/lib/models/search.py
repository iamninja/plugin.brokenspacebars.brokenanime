# -*- coding: utf-8 -*-

class SearchResults():
    def __init__(self, data):
        self.total = data['pageInfo']['total'] if 'total' in data['pageInfo'].keys() else None
        self.perPage = data['pageInfo']['perPage'] if 'perPage' in data['pageInfo'].keys() else None
        self.currentPage = data['pageInfo']['currentPage'] if 'currentPage' in data['pageInfo'].keys() else None
        self.lastPage = data['pageInfo']['lastPage'] if 'lastPage' in data['pageInfo'].keys() else None
        self.hasNextPage = data['pageInfo']['hasNextPage'] if 'hasNextPage' in data['pageInfo'].keys() else None

# TODO: Trailer needs work (multi source: yt, dailym, etc?)
class AnimeResult():
    def __init__(self, data):
        self.id = data['id']
        self.idMal = data['idMal']
        # title {
        #     romaji
        #     english
        #     native
        #     userPreferred
        # }
        self.title = data['title']
        self.status = data['status']
        self.synonyms = data['synonyms']
        self.description = data['description']
        # Year
        self.year = data['startDate']['year']
        # coverImage {
        #     extraLarge
        #     large
        #     medium
        #     color
        # }
        self.coverImage = data['coverImage']['large']
        self.bannerImage = data['bannerImage']
        # if 'id' in data['trailer'].keys():
        #     self.trailer = data['trailer']['id']
        self.mediaListEntryId = data['mediaListEntry']['id'] if data['mediaListEntry'] is not None else None

    def getAnimeInfo(self):
        return {
            'plot': self.description,
            'title': self.title['userPreferred'],
            'premiered': self.year,
            'status': self.status,
            'mediatype': "tvshow",
            # 'trailer': "https://www.youtube.com/watch?v=" + str(self.trailer) if hasattr(self, 'trailer') else ""
        }

    def getAnimeArt(self):
        return {
            'fanart': self.coverImage,
            'thumb': self.bannerImage
        }

class AnimeResults(SearchResults):
    def __init__(self, data):
        SearchResults.__init__(self, data)
        self.list = []
        for anime in data['resultsAnime']:
            self.list.append(AnimeResult(anime))
