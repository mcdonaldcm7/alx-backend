#!/usr/bin/env python3
"""
Tasks

3. Deletion-resilient hypermedia pagination

The goal here is that if between two queries, certain rows are removed from the
dataset, the user does not miss items from dataset when changing page.

Implement a 'get_hyper_index' method with two integer arguments: 'index' with a
'None' default value and 'page_size' with default value of 10.

The method should return a dictionary with the following key-value pairs:
    - 'index': the current start index of the return page. That is the index of
    the first item in the current page. For example if requesting page 3 with
    'page_size' 20, and no data was removed from the dataset, the current index
    should be 60.
    - 'next_index': the next index to query with. That should be the index of
    the first item after the last item on the current page.
    - 'page_size': the current page size
    - 'data': the actual page of the dataset

Requirements/Behavior:

    - Use 'assert' to verify that 'index' is in a valid range.
    - If the user queries index 0, 'page_size' 10, they will get rows indexed 0
    to 9 included.
    - If they request the next index (10) with 'page_size' 10, but rows 3, 6
    and 7 were deleted, the user should still receive rows indexed 10 to 19
    included.
"""
import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns a dictionary with key-value pair information for the requested
        page
        """
        full_data = self.indexed_dataset()

        assert index is not None and index >= 0 and index <= len(full_data)

        data = {}
        next_index = index
        length = index + page_size
        i = index
        while i < length:
            temp = full_data.get(i)
            if temp is not None:
                data[i] = temp
            else:
                length += 1
            next_index = i + 1
            i += 1
        return {
                "next_index": next_index,
                "data": list(data.values()),
                "index": index,
                "page_size": page_size
                }
