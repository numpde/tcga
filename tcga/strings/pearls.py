# RA, 2020-06-17

import typing


def kplets(k: int, s: str, no_remainder=True) -> typing.Iterable[str]:
    """
    When k = 3, from a string like s = 'GCATCGAGC'
    generate the triples 'GCA', 'TCG', 'AGC'.
    Similarly for other k >= 1.
    The string must have length divisible by k
    when no_remainder is True; otherwise
    the trailing characters are ignored.
    """
    assert (k >= 1)

    if no_remainder and (len(s) % k):
        raise ValueError(F"The string should have length a multiple of {k}")

    for n in range(0, (len(s) // k) * k, k):
        yield s[n:(n + k)]


def triplets(s: str) -> typing.Iterable[str]:
    """
    From a string like s = 'GCATCGAGC'
    generate the triples 'GCA', 'TCG', 'AGC'.
    """
    yield from kplets(3, s, no_remainder=True)


def reverse(s: str) -> str:
    """
    For a string s return the reversed string s[::-1].
    """
    return s[::-1]


def lines(s: str) -> typing.Iterable[str]:
    """
    Split the string at '\n' and yield the lines.
    Applies str.strip to each line.
    """
    yield from map(str.strip, s.strip().split('\n'))


def nnna(s: str, n=3, m=1) -> typing.Iterable[typing.Tuple[str, str]]:
    """
    Takes a string like
        UUU F UUC F ...
    where white spaces and new lines are ignored.

    Generates tuples
        ('UUU', 'F'), ('UUC', 'F'), ...
    """
    assert (n >= 0) and (m >= 0) and (n + m >= 1)

    import re
    s = re.sub(r"\s+", "", s)

    if (len(s) % (n + m)):
        raise ValueError(F"The string's length {len(s)} (ignoring whitespace) is not a multiple of (n + m) = {n + m}.")

    from tcga.utils import First
    f = First(lambda x: kplets(n + m, x)).each(lambda x: (x[0:n], x[n:(n + m)]))

    yield from f(s)
