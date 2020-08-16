# -*- coding: utf-8 -*-

import re
import requests
import time
from bs4 import BeautifulSoup

baseURL = "https://www.gogoanime1.com/watch/detective-conan/episode/episode-"

def get_mp4_for_conan(episode):
    print(baseURL + str(episode))
    resp = requests.get(baseURL + str(episode))
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, 'html.parser')
    vid = soup.find_all("script")[10].prettify()
    match = re.findall(r'\"(.+?)\"',vid)
    # resp2 = requests.get(match[0])
    # print("-----" + resp2.status_code)
    # print("sleeping")
    # time.sleep(60)
    if match:
        print(match[0])
    else:
        print("Not Found")
    # print(vid)
    
    return match[0]
