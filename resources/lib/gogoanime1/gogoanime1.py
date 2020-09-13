# -*- coding: utf-8 -*-

import re
import requests
import time
import random
import logging
from urllib import quote

from bs4 import BeautifulSoup
import xbmcaddon

from resources.lib.utils import kodilogging

conanURL = "https://www.gogoanime1.com/watch/detective-conan/episode/episode-"
baseURL = "https://www.gogoanime1.com/watch/"

# TODO: Clean comments

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()

def get_mp4_for_conan(episode):
    logger.debug(conanURL + str(episode))
    resp = requests.get(baseURL + str(episode))
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, 'html.parser')
    vid = soup.find_all("script")[10].prettify()
    match = re.findall(r'\"(.+?)\"', vid)
    # resp2 = requests.get(match[0])
    # logger.debug("-----" + resp2.status_code)
    # logger.debug("sleeping")
    # time.sleep(60)
    if match:
        logger.debug(match[0])
    else:
        logger.debug("Not Found")
    # logger.debug(vid)

    return match[0]

def get_mp4(slug, episode):
    logger.debug("----------get_mp4()----------")
    logger.debug(baseURL + str(slug) + "/episode/episode-" + str(episode))
    resp = requests.get(baseURL + str(slug) + "/episode/episode-" + str(episode))
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, 'html.parser')
    if not soup.find('div', class_='vmn-player'):
        return None
    vid = soup.find_all("script")[10].prettify()
    match = re.findall(r'\"(.+?)\"',vid)
    # logger.debug(vid)
    if match:
        logger.debug(match[0])
    else:
        logger.debug("Not Found")
        return
    # Add random
    # url = match[0].replace('https', 'http')
    # urls = generate_random_urls(url)

    # return urls
    return [match[0]]

def generate_random_urls(url):
    end_part = url.split("anime1.com/")[1]
    urls = [url]
    for i in (1,3):
        urls.append("https://st" + str(random.randint(6, 12)) + ".anime1.com/" + end_part)
    return urls

def get_latest_episode_number(slug):
    resp = requests.get(baseURL + str(slug))
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, 'html.parser')
    # latest_episode = soup.find("div", class_="epCheck").find_next('a').get('href').split("-")[-1]
    latest_episode = soup.find_all('a', text=re.compile("Episode"))[1].get('href').split('-')[-1]
    logger.debug("Latest episode found for " + str(slug) + " is " + str(latest_episode))
    return latest_episode


