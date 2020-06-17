# RA, 2020-06-17

from typing import Callable


class First:
    """
    Example:
        f = First(list.pop).then(str.lower).then(tuple)
        assert f(["ABC", "XYZ"]) == ('x', 'y', 'z')
    """

    def __init__(self, f):
        self.__ff = []
        self.then(f)

    def then(self, f):
        if isinstance(f, Callable):
            self.__ff.append(f)
            return self

        if hasattr(f, "__getitem__"):
            self.__ff.append(f.__getitem__)
            return self

        raise RuntimeError("It appears that the passed object f supports neither f(-) nor f[-].")

    def __matmul__(self, other):
        return First(other).then(self)

    def __call__(self, x):
        for f in self.__ff:
            x = f(x)
        return x

    def __getitem__(self, x):
        return self(x)
