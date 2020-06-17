# RA, 2020-06-17

from typing import Union, Iterable
from itertools import chain


def circular_windows(v: slice, n: int) -> Iterable[slice]:
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


class CircularView:
    def __init__(self, x: Union[str, list, tuple]):
        self.x = x
        self._i = None

    def __getitem__(self, key):
        if isinstance(key, slice):
            key.indices(1)

            parts = (self.x[w] for w in circular_windows(key, len(self.x)))

            if isinstance(self.x, str):
                return ''.join(parts)
            if isinstance(self.x, list):
                return list(chain.from_iterable(parts))
            if isinstance(self.x, tuple):
                return tuple(chain.from_iterable(parts))

        if isinstance(key, int):
            return self.x[key % len(self.x)]

        raise NotImplementedError


if __name__ == '__main__':
    S = "a string"
    assert S[3:1] == ""

    for n in range(-10, 30):
        assert CircularView(S)[n] == S[n % len(S)]

    assert CircularView(S)[3:1] == S[3:1]

    v = slice(-3, 5, 2)
    s = "ABC"
    print(F"If v = {v} and s = '{s}' then")
    print(F"    [s[w] for w in circular_windows(v, len(s))]")
    print(F"is")
    print(F"    {[s[w] for w in circular_windows(v, len(s))]}")

    print(F"Examples of {CircularView.__name__}:")
    for n in range(0, 30):
        a = -n // 2
        b = n
        s = CircularView(S)[a:b:2]
        print(F'{CircularView.__name__}("{S}")[{a}:{b}:2] is "{s}"')
