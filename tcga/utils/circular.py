# RA, 2020-06-17

import tcga.utils
import typing


def circular_windows(v: slice, n: int) -> typing.Iterable[slice]:
    """
    For an extended slice `v`, generate a set of slices
    for a sequence of length `n`, so that they
    together make up `v`.

    For example, if
        v = slice(-3, 5, 2)  and  n = 3
    then yield the slices
        [slice(0, 3, 2), slice(1, 3, 2), slice(0, 2, 2)]
    In particular, if
        s = 'ABC'
    then
        [s[w] for w in circular_windows(v, len(s))]
    is the list
        ['AC', 'B', 'A']
    because those compose the slice `v`:
       -3  01234
        * * * *
        ABCABCABC
    """

    (a, b, s) = (v.start, v.stop, v.step)

    assert isinstance(n, int), "The length of the sequence/string is an integer"
    assert (n >= 0), "The length of the sequence/string must be nonnegative"

    empty = slice(0, 0)

    if (n <= 0):
        yield empty
        return

    if (b <= a) and (s is None):
        yield empty
        return

    if (a <= b) and ((s is not None) and (s < 0)):
        yield empty
        return

    if (b <= a) and ((s is not None) and (s > 0)):
        yield empty
        return

    # Simple forward case
    if (a <= b) and ((s is None) or (s == 1)):
        d = b - a
        while d:
            a = a % n
            i = (min(n, a + d) - a)
            yield slice(a, a + i)
            d -= i
            a += i
        return

    # Forward case with positive step
    if (a <= b) and (s > 0):
        d = b - a
        a = a % n
        while d > 0:
            b = min(n, a + d)
            assert (0 <= a < b <= n)
            yield slice(a, b, s)
            if (b - a) % s:
                b += s - (b - a) % s
            d -= (b - a)
            a += (b - a) - n
        return

    # Backward case
    if (b < a) and (s < 0):
        d = b - a
        a = a % n
        while d < 0:
            b = max(-1, a + d)
            yield slice(a, max(b, 0), s)
            if (b == -1) and not (a % s):
                yield slice(0, 1)
            if (b - a) % s:
                b += s - (b - a) % s
            d -= (b - a)
            a += (b - a) + n
        return

    raise NotImplementedError


class _Laola:
    class Viewer:
        def __init__(self, key):
            self.key = key

        def __call__(self, x: typing.Union[str, list, tuple]):
            if isinstance(self.key, slice):
                self.key.indices(1)
                parts = (x[w] for w in circular_windows(self.key, len(x)))
                return tcga.utils.join[type(x)](parts)

            if isinstance(self.key, int):
                return x[self.key % len(x)]

            raise NotImplementedError

    def __getitem__(self, key):
        return _Laola.Viewer(key)


laola = _Laola()


class Circular:
    """
    Provides a view of a string/list/tuple
    pretending that it is circular.

    For example,
        Circular("ABC")[-3:5:2]
    returns
        "ACBA"
    because:
        ABCABCABC
       -3  012345
        * * * *

    The view returns a shallow copy.

    Note: len/str/repr refer to the original.
    """

    def __init__(self, x):
        self.x = x

    def __getitem__(self, key):
        return laola[key](self.x)

    def __len__(self):
        return len(self.x)

    def __repr__(self):
        return F"{type(self).__name__}({repr(self.x)})"


def _example():
    S = "a string"
    assert S[3:1] == ""

    for n in range(-10, 30):
        assert Circular(S)[n] == S[n % len(S)]

    assert Circular(S)[3:1] == S[3:1]

    #
    print("Example 1")

    w = laola[-3:5:2]
    s = "ABC"
    print(F"If w = laola[-3:5:2] and s = '{s}' then")
    print(F"    w(s) = '{w(s)}'")

    #
    print("Example 2")

    v = slice(-3, 5, 2)
    s = "ABC"
    print(F"If v = {v} and s = '{s}' then")
    print(F"    [s[w] for w in circular_windows(v, len(s))]")
    print(F"is")
    print(F"    {[s[w] for w in circular_windows(v, len(s))]}")

    #
    print(F"Examples of {Circular.__name__}:")

    for n in range(0, 30):
        a = -n // 2
        b = n
        s = Circular(S)
        print(F"{s}[{a}:{b}:2] is '{s[a:b:2]}'")


if __name__ == '__main__':
    _example()
