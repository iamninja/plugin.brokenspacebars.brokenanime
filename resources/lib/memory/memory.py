# -*- coding: utf-8 -*-

import pickle
# from future.utils import iteritems
from collections.abc import MutableMapping

import xbmcgui

class MemoryStorage(MutableMapping):


    def __init__(self, storage_id, window_id=10000):
        self._id = storage_id
        self._window = xbmcgui.Window(window_id)
        try:
            self['__keys__']
        except KeyError:
            self['__keys__'] = []

    def _format_contents(self):
        lines = []
        for key, val in map(self):
            lines.append('{0}: {1}'.format(repr(key), repr(val)))
        return ', '.join(lines)

    def __str__(self):
        return '<MemStorage {{{0}}}>'.format(self._format_contents())

    def __getitem__(self, key):
        full_key = '{0}_{1}'.format(self._id, key)
        raw_item = self._window.getProperty(full_key)
        if raw_item:
            try:
                return pickle.loads(bytes(raw_item))
            except TypeError as e:
                return pickle.loads(bytes(raw_item, 'utf-8'))
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        full_key = '{0}_{1}'.format(self._id, key)
        self._window.setProperty(full_key, pickle.dumps(value, protocol=0))
        keys = self['__keys__']
        if key != '__keys__' and key not in keys:
            keys.append(key)
            self['__keys__'] = keys

    def __delitem__(self, key):
        full_key = '{0}_{1}'.format(self._id, key)
        item = self._window.getProperty(full_key)
        if item:
            self._window.clearProperty(full_key)
            if key != '__keys__':
                keys = self['__keys__']
                keys.remove(key)
                self['__keys__'] = keys
            else:
                raise KeyError(key)

    def __contains__(self, key):
        full_key = '{0}_{1}'.format(self._id, key)
        item = self._window.getProperty(full_key)
        return bool(item)

    def __iter__(self):
        return iter(self['__keys__'])

    def __len__(self):
        return len(self['__keys__'])
