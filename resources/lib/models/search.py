# -*- coding: utf-8 -*-

class SearchResults():
    def __init__(self, data):
        self.total = data['pageInfo']['total'] if 'total' in data['pageInfo'].keys() else None
        self.perPage = data['pageInfo']['perPage'] if 'perPage' in data['pageInfo'].keys() else None
        self.currentPage = data['pageInfo']['currentPage'] if 'currentPage' in data['pageInfo'].keys() else None
        self.lastPage = data['pageInfo']['lastPage'] if 'lastPage' in data['pageInfo'].keys() else None
        self.hasNextPage = data['pageInfo']['hasNextPage'] if 'hasNextPage' in data['pageInfo'].keys() else None

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
        self.coverImage = data['coverImage']
        self.bannerImage = data['bannerImage']
        self.mediaListEntryId = data['mediaListEntry']['id'] if data['mediaListEntry'] is not None else None

class AnimeResults(SearchResults):
    def __init__(self, data):
        SearchResults.__init__(self, data)
        self.list = []
        for anime in data['resultsAnime']:
            self.list.append(AnimeResult(anime))
