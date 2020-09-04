# -*- coding: utf-8 -*-

# import logging
import time

import xbmc

# from service import server


# logger = logging.getLogger('plugin.brokenspacebars.brokenanime')
# server.run()

print("SERVICE IS TAKING CONTROL")
while True:
    if xbmc.Player().isPlaying():
        print("Playing something!!!!")

    else:
        print("Not playing :(")

    time.sleep(10)

