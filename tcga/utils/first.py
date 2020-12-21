# RA, 2020-06-17

import typing
import itertools


class _:
    class Join:
        def __init__(self, as_type=str):
            self._result_type = as_type

        def __getitem__(self, as_type=str):
            return _.Join(as_type)

        def __call__(self, iterable: typing.Iterable):
            if self._result_type is str:
                return ''.join(itertools.chain.from_iterable(iterable))
            else:
                return self._result_type(itertools.chain.from_iterable(iterable))


class First:
    """
    Example:
        f = First(list.pop).then(str.lower).then(tuple)
        assert f(["ABC", "XYZ"]) == ('x', 'y', 'z')
    """

    @classmethod
    def _as_callable(cls, f):
        if isinstance(f, typing.Callable):
            return f
        if hasattr(f, "__getitem__"):
            return f.__getitem__
        raise RuntimeError("It appears that the passed object f supports neither f(-) nor f[-].")

    def __init__(self, f):
        self.__ff = []
        self.then(f)

    def then(self, f):
        self.__ff.append(self._as_callable(f))
        return self

    def each(self, f):
        self.__ff.append(
            lambda c: map(self._as_callable(f), c)
        )
        return self

    def keep(self, predicate=None):
        """
        Performs
            filter(predicate, .)

        In particular, if `predicate` is None,
        keeps only the truthy elements.
        """
        self.__ff.append(
            lambda c: filter(
                self._as_callable(predicate) if (predicate is not None) else None,
                c
            )
        )
        return self

    def join(self, as_type):
        self.__ff.append(_.Join(as_type))
        return self

    def dict(self, keys) -> dict:
        """
        Convert to a dictionary on `keys`.
        """
        return {k: self(k) for k in keys}

    def __matmul__(self, other):
        return First(other).then(self)

    def __call__(self, x):
        for f in self.__ff:
            x = f(x)
        return x

    def __getitem__(self, x):
        return self(x)


join = _.Join()
