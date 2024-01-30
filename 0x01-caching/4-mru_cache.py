#!/usr/bin/env python3
"""
Task

4. MRU Caching

Create a class 'MRUCache' that inherits from 'BaseCaching' and is a caching
system:

    - You must use 'self.cache_data' - dictionary from the parent class
    'BaseCaching'
    - You can overload 'def __init__(self):' but don’t forget to call the
    parent init: 'super().__init__()'
    - def put(self, key, item):
        * Must assign to the dictionary 'self.cache_data' the 'item' value for
        the key 'key'.
        * If 'key' or 'item' is 'None', this method should not do anything.
        * If the number of items in 'self.cache_data' is higher that
        'BaseCaching.MAX_ITEMS':
            - you must discard the most recently used item (MRU algorithm)
            - you must print 'DISCARD:' with the 'key' discarded and followed
            by a new line
    - def get(self, key):
        * Must return the value in 'self.cache_data' linked to 'key'.
        * If 'key' is 'None' or if the 'key' doesn’t exist in
        'self.cache_data', return None.
"""


BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """
    A MOST RECENTLY USED cache policy implementation
    """

    def __init__(self):
        super().__init__()
        self._recently_used_key = [None, None]

    def put(self, key, item):
        """
        Puts a key and it's corresponding value item in the dictionary (cache)
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

            if len(self.cache_data) > self.MAX_ITEMS:
                if self._recently_used_key[0] is not None:
                    del self.cache_data[self._recently_used_key[0]]
                    print('DISCARD: {}'.format(self._recently_used_key[0]))
                    self._recently_used_key[0] = None
                else:
                    del self.cache_data[self._recently_used_key[1]]
                    print('DISCARD: {}'.format(self._recently_used_key[1]))
            self._recently_used_key[1] = key

    def get(self, key):
        """
        Returns the value associated with the key `key`
        """
        if key is not None and key in self.cache_data:
            self._recently_used_key[0] = key
            return self.cache_data[key]
        return None
