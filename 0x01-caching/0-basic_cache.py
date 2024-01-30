#!/usr/bin/env python3
"""
Task

0. Basic dictionary
Create a class BasicCache that inherits from BaseCaching and is a caching
system:

    - You must use self.cache_data - dictionary from the parent class
    BaseCaching
    - This caching system doesn’t have limit
    - def put(self, key, item):
        * Must assign to the dictionary self.cache_data the item value for the
        key key.
        * If key or item is None, this method should not do anything.
    - def get(self, key):
        * Must return the value in self.cache_data linked to key.
        * If key is None or if the key doesn’t exist in self.cache_data, return
        None.
"""


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache (BaseCaching):
    """
    Inherits from the BaseCaching class add custom implementations to the
    inheritted methods
    """

    def put(self, key, item):
        """
        Adds a key and it's value pair to the dictionary
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieves the value associated with the key `key` or None if key is
        None or doesn't exists
        """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
