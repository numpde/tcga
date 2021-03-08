# RA, 2020-10-09
# RA, 2020-12-06

def from_iterable(X, type=None):
    from itertools import chain
    if type is None:
        return chain.from_iterable(X)
    else:
        return type(chain.from_iterable(X))


def first(X):
    """
    Returns the first element of an iterable X.
    """
    return next(iter(X))


def at_most_n(X, n=-1):
    """
    Yields at most n elements from iterable X.
    All elements if n equals -1.
    No elements if n is None.
    """
    if n is None:
        pass
    elif (n == -1):
        yield from X
    else:
        for (x, __) in zip(X, range(n)):
            yield x


def unlist1(L):
    """
    Check that L has only one element at return it.
    """
    L = list(L)
    if not (len(L) == 1):
        raise ValueError(F"Expected an iterable of length 1, got {len(L)}.")
    return L[0]


def pretty(x):
    """
    Return a formatted JSON string of `x`.
    """
    import json
    return json.dumps(x, indent=2)


class minidict:
    """
    A slim read-only dictionary.
    """

    def __init__(self, data: dict):
        self._data = dict(data)

    def __repr__(self):
        return repr(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __len__(self):
        return len(self._data)

    def keys(self):
        return self._data.keys()

    def items(self):
        return zip(self._data.keys(), map(self.__getitem__, self._data.keys()))

    def __contains__(self, item):
        return (item in self._data)
