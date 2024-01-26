#!/usr/bin/env python3
"""
Task

1. Simple pagination

Implement a method named 'get_page' that takes two integer arguments 'page'
with default value 1 and 'page_size' with default value 10.

    - You have to use the CSV file provided at the top of the project
    - Use 'assert' to verify that both arguments are integers greater than 0.
    - Use 'index_range' to find the correct indexes to paginate the dataset
    correctly and return the appropriate page of the dataset (i.e. the correct
    list of rows).
    - If the input arguments are out of range for the dataset, an empty list
    should be returned.
"""
import csv
import math
from typing import List


def index_range(page, page_size):
    """
    Returns a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for those
    particular pagination parameters
    """
    start_index = page_size * (page - 1)
    end_index = page_size * page
    return (start_index, end_index)


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns the appropriate page of the dataset (i.e. the correct list of
        rows)
        """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        indexes = index_range(page, page_size)
        pages = []

        if (indexes[0]) > len(self.dataset()):
            return pages
        for i in range(page_size):
            pages.append(self.__dataset[indexes[0] + i])

        return pages
