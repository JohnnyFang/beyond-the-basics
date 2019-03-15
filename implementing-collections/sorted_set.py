class SortedSet:

    def __init__(self, items=None):
        """
        we use deliberately use None as the default argument, rather than an empty list to avoid inadvertently mutating
        the default argument object, which is created one when the method is first defined
        :param items:
        """
        self._items = sorted(items) if items is not None else []
