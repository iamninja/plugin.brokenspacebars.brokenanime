# -*- coding: utf-8 -*-

from time import time
from resources.lib.utils.textformat import secondsToRemaining

class LatestEpisodeInfo():
    def __init__(self, data):
        print(data)
        self.anilistId = data['data']['Media']['id']
        self.title = data['data']['Media']['title']['userPreferred']
        self.status = data['data']['Media']['status']
        self.episodes = data['data']['Media']['episodes']
        self.nextEpisode = data['data']['Media']['nextAiringEpisode']['episode']
        self.latestEpisode = self.nextEpisode - 1
        self.nextAiringAt = self._remaingToNextEpisode(data['data']['Media']['nextAiringEpisode']['airingAt'])

    def _remaingToNextEpisode(self, nextEpisode):
        remainingSeconds = int(nextEpisode) - int(time())
        return secondsToRemaining(remainingSeconds)