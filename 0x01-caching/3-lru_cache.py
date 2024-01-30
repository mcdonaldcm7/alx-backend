#!/usr/bin/env python3
"""
Task

3. LRU Caching

Create a class 'LRUCache' that inherits from 'BaseCaching' and is a caching
system:

    - You must use 'self.cache_data' - dictionary from the parent class
    'BaseCaching'
    - You can overload 'def __init__(self):' but don’t forget to call the
    parent init: 'super().__init__()'
    - def put(self, key, item):
        * Must assign to the dictionary 'self.cache_data' the item value for
        the key 'key'.
        * If 'key' or 'item' is 'None', this method should not do anything.
        * If the number of items in 'self.cache_data' is higher that
        'BaseCaching.MAX_ITEMS':
            - you must discard the least recently used item (LRU algorithm)
            - you must print 'DISCARD:' with the 'key' discarded and followed
            by a new line
    - def get(self, key):
        * Must return the value in 'self.cache_data' linked to 'key'.
        * If 'key' is 'None' or if the 'key' doesn’t exist in
        'self.cache_data', return 'None'.
"""


BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    A LEAST RECENTLY USED cache policy implementation
    """

    def __init__(self):
        super().__init__()
        self._keys_use = {}

    def put(self, key, item):
        """
        Puts a key and it's corresponding value item in the dictionary (cache)
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

            freq = None
            for freq_key in self._keys_use:
                if freq is None:
                    freq = self._keys_use[freq_key]
                elif freq < self._keys_use[freq_key]:
                    freq = self._keys_use[freq_key]

            if key not in self._keys_use:
                self._keys_use[key] = (
                        freq if freq is not None and freq > 0 else 1) + 1
            else:
                self._keys_use[key] = freq + 1

            for freq_key in self._keys_use:
                if freq_key != key:
                    self._keys_use[freq_key] -= 1

            if len(self.cache_data) > self.MAX_ITEMS:
                freq = None
                lru_key = None

                for key_freq in self._keys_use:
                    if freq is None:
                        freq = self._keys_use[key_freq]
                        lru_key = key_freq
                    if freq is not None and self._keys_use[key_freq] < freq:
                        freq = self._keys_use[key_freq]
                        lru_key = key_freq

                del self.cache_data[lru_key]
                del self._keys_use[lru_key]
                print('DISCARD: {}'.format(lru_key))

    def get(self, key):
        """
        Returns the value associated with the key `key`
        """
        if key is not None and key in self.cache_data:
            freq = None
            for freq_key in self._keys_use:
                if freq is None:
                    freq = self._keys_use[freq_key]
                elif freq < self._keys_use[freq_key]:
                    freq = self._keys_use[freq_key]
                self._keys_use[freq_key] -= 1

            self._keys_use[key] = freq + 1
            return self.cache_data[key]
        return None
