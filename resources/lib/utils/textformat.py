# -*- coding: utf-8 -*-

def secondsToRemaining(time):
    time = float(time)
    days = time // (24 * 3600)
    time %= 24 * 3600
    hours = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    string = '{d}d {h}h {m}m {s}s'.format(
        d = int(days), h = int(hours), m = int(minutes), s = int(seconds))
    return string

def createSlug(string):
    return string.replace(' ', '-')

def unicode_sandwich(string):
    return u' '.join(string).encode('utf-8').strip()

def color_label(string, color):
    return '[COLOR ' + color + ']' + string + '[/COLOR]'
