#!/usr/bin/env python3
"""
Task

2. Hypermedia pagination

Replicate code from the previous task.

Implement a 'get_hyper' method that takes the same arguments (and defaults) as
'get_page' and returns a dictionary containing the following key-value pairs:

    - 'page_size': the length of the returned dataset page
    - 'page': the current page number
    - 'data': the dataset page (equivalent to return from previous task)
    - 'next_page': number of the next page, 'None' if no next page
    - 'prev_page': number of the previous page, 'None' if no previous page
    - 'total_pages': the total number of pages in the dataset as an integer

Make sure to reuse get_page in your implementation.

You can use the 'math' module if necessary
"""
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> type(int):
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

        if indexes[0] > len(self.dataset()):
            return pages
        for i in range(page_size):
            pages.append(self.__dataset[indexes[0] + i])

        return pages

    def get_hyper(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns page information
        """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        pages = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.__dataset) / page_size)
        next_page = (page + 1) if (page + 1) < (total_pages - 1) else None
        prev_page = (page - 1) if (page - 1) > 0 else None

        if len(pages) == 0:
            indexes = index_range(page, page_size)
            if indexes[0] > len(self.__dataset):
                return {'page_size': 0, 'page': page, 'data': pages,
                        'next_page': None, 'prev_page': prev_page,
                        'total_pages': total_pages}

        hyper = {'page_size': page_size, 'page': page, 'data': pages,
                 'next_page': next_page, 'prev_page': prev_page,
                 'total_pages': total_pages}
        return hyper
