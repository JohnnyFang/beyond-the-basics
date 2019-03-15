from collections.abc import Sequence


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
        return item in self._items

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
