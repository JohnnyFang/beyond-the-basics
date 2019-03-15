from bisect import bisect_left
from collections.abc import Sequence
from itertools import chain


class SortedSet(Sequence):

    def __init__(self, items=None):
        """
        we use deliberately use None as the default argument, rather than an empty list to avoid inadvertently mutating
        the default argument object, which is created one when the method is first defined
        :param items:
        """
        self._items = sorted(set(items)) if items is not None else []

    def __contains__(self, item):
        """
        container protocol!
        :param item:
        :return:
        """
        try:
            self.index(item)
            return True
        except ValueError:
            return False

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)
        # or
        # for item in self._items:
        #    yield item

    def __getitem__(self, index):
        result = self._items[index]
        return SortedSet(result) if isinstance(index, slice) else result

    def __repr__(self):
        return "SortedSet({})".format(repr(self._items) if self._items else '')

    def __eq__(self, rhs):
        if not isinstance(rhs, SortedSet):
            return NotImplemented
        return self._items == rhs._items

    def __ne__(self, rhs):
        """
        the Python docs are clear that when specializing the __eq__ in a subclass, we must also
        specialize __ne__
        :param rhs:
        :return:
        """
        if not isinstance(rhs, SortedSet):
            return NotImplemented
        return self._items != rhs._items

    def index(self, item):
        """
        we make use of binary search - bisect_left
        :param item:
        :return:
        """
        index = bisect_left(self._items, item)
        if (index != len(self._items)) and (self._items[index] == item):
            return index
        raise ValueError("{} not found".format(repr(item)))

    def count(self, item):
        return int(item in self)

    def __add__(self, rhs):
        """
        concatenation
        :param other:
        :return:
        """
        return SortedSet(chain(self._items, rhs._items))

    def __mul__(self, rhs):
        """
        Repetition Protocol
        :param rhs:
        :return:
        """
        return self if rhs > 0 else SortedSet()

    def __rmul__(self, lhs):
        """
        Repetition Protocol
        :param rhs:
        :return:
        """
        return self * lhs
