#!/usr/bin/env python3
"""
Task

1. FIFO caching

Create a class 'FIFOCache' that inherits from 'BaseCaching' and is a caching
system:

    - You must use 'self.cache_data' - dictionary from the parent class
    'BaseCaching'
    - You can overload 'def __init__(self):' but don’t forget to call the
    parent init: 'super().__init__()'
    - 'def put(self, key, item):'
        * Must assign to the dictionary 'self.cache_data' the item value for
        the key 'key'.
        * If 'key' or 'item' is 'None', this method should not do anything.
        * If the number of items in 'self.cache_data' is higher that
        'BaseCaching.MAX_ITEMS':
            - you must discard the first item put in cache (FIFO algorithm)
            - you must print 'DISCARD': with the 'key' discarded and following
            by a new line
    - 'def get(self, key):'
        * Must return the value in self.cache_data linked to key.
        * If 'key' is 'None' or if the 'key' doesn’t exist in
        'self.cache_data', return 'None'.
"""


BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    A FIRST IN FIRST OUT cache policy implementation
    """

    def __init__(self):
        super().__init__()
        self._keys = []

    def put(self, key, item):
        """
        Puts a key and it's corresponding value item in the dictionary (cache)
        If the number of items in the dictionary is higher than
        BaseCaching.MAX_ITEMS. Discard the first item put in the cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item
            self._keys.append(key)
            if len(self.cache_data) > self.MAX_ITEMS:
                discard = self._keys.pop(0)
                del self.cache_data[discard]
                print('DISCARD: {}'.format(discard))

    def get(self, key):
        """
        Returns the value associated with the key `key`
        """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
