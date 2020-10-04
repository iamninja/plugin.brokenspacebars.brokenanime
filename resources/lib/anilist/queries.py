# -*- coding: utf-8 -*-

# Search anilist api for anime using slug
# and returns next airing episode
# variables: $querystring: String
# example: { 'queryString': "one-piece" }
# example response:
# {
#   "data": {
#     "Media": {
#       "id": 21,
#       "title": {
#         "romaji": "One Piece",
#         "english": "One Piece",
#         "native": "ワンピース",
#         "userPreferred": "One Piece"
#       },
#       "status": "RELEASING",
#       "episodes": null,
#       "nextAiringEpisode": {
#         "id": 288400,
#         "episode": 939,
#         "airingAt": 1598747400
#       }
#     }
#   }
# }
queryForNextEpisode = '''
    query ($queryString: String) {
        Media(search: $queryString, type: ANIME) {
            id
            title {
                romaji
                english
                native
                userPreferred
            }
            status
            episodes
            nextAiringEpisode {
                id
                episode
                airingAt
            }
        }
    }
'''
# Get currently watching anime from anilist
# variables: $userName: String
# example: { 'userName': "iamninja" }
# example response:
# "MediaListCollection": {
#       "lists": [
#         {
#           "name": "Watching",
#           "status": "CURRENT",
#           "entries": [
#             {
#               "id": 133903055,
#               "progress": 10,
#               "media": {
#                 "id": 103572,
#                 "episodes": 12,
#                 "title": {
#                   "userPreferred": "5-Toubun no Hanayome"
#                 },
#                 "status": "FINISHED",
#                 "nextAiringEpisode": null
#               }
#             },
#             {
#               "id": 133903056,
#               "progress": 10,
#               "media": {
#                 "id": 20639,
#                 "episodes": 23,
#                 "title": {
#                   "userPreferred": "Abarenbou Rikishi!! Matsutarou"
#                 },
#                 "status": "FINISHED",
#                 "nextAiringEpisode": null
#               }
#             },
#             ...
#           ]
#        }
#       ]
# }
queryForWatchingAnime = '''
    query ($userName: String) {
        MediaListCollection(userName: $userName, type: ANIME, status:CURRENT) {
            lists {
                name
                status
                entries {
                    id
                    progress
                    media {
                        id
                        episodes
                        title {
                            english
                            romaji
                            native
                            userPreferred
                        }
                        synonyms
                        description
                        status
                        source
                        format
                        averageScore
                        isAdult
                        duration
                        type
                        startDate {
                            year
                            month
                            day
                        }
                        endDate {
                            year
                            month
                            day
                        }
                        coverImage {
                            extraLarge
                            large
                            medium
                            color
                        }
                        bannerImage
                        nextAiringEpisode {
                            id
                            episode
                            airingAt
                        }
                    }
                }
            }
        }
    }
'''
# TODO: Needs documentaion
queryForAnimeInList = '''
    query ($id: Int) {
        MediaList(id: $id) {
            id
            progress
            media {
                id
                episodes
                title {
                    english
                    romaji
                    native
                    userPreferred
                }
                synonyms
                description
                status
                source
                format
                averageScore
                isAdult
                duration
                type
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                coverImage {
                    extraLarge
                    large
                    medium
                    color
                }
                bannerImage
                nextAiringEpisode {
                    id
                    episode
                    airingAt
                }
            }
        }
    }
'''

# TODO: Needs documentaion
queryForAnime = '''
    query ($id: Int) {
        media: Media(id: $id) {
            id
            episodes
            title {
                english
                romaji
                native
                userPreferred
            }
            synonyms
            description
            status
            source
            format
            averageScore
            isAdult
            duration
            type
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            coverImage {
                extraLarge
                large
                medium
                color
            }
            bannerImage
            nextAiringEpisode {
                id
                episode
                airingAt
            }
        }
    }
'''

# Search anilist api for anime using slug
# and returns next airing episode
# variables: $querystring: String
# example: { 'queryString': "one-piece" }
# example response:
# {
#   "data": {
#     "Media": {
#       "id": 21,
#       "title": {
#         "romaji": "One Piece",
#         "english": "One Piece",
#         "native": "ワンピース",
#         "userPreferred": "One Piece"
#       },
#       "status": "RELEASING",
#       "episodes": null,
#       "nextAiringEpisode": {
#         "id": 288400,
#         "episode": 939,
#         "airingAt": 1598747400
#       }
#     }
#   }
# }
querySearchAnime = '''
    query ($query: String) {
        Page(perPage: 15) {
            pageInfo {
                total
            }
            resultsAnime:media(search: $query, type: ANIME) {
                id
                idMal
                title {
                    romaji
                    english
                    native
                    userPreferred
                }
                status
                synonyms
                description
                startDate {
                    year
                }
                coverImage {
                    extraLarge
                    large
                    medium
                    color
                }
                bannerImage
                trailer {
                    id
                    site
                }
                mediaListEntry {
                    id
                }
            }
        }
    }
'''
