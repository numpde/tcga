# RA, 2020-06-17

import typing


def kplets(k: int, s: str) -> typing.Iterable[str]:
    if (len(s) % k):
        raise ValueError(F"The string should have length a multiple of {k}")
    for n in range(0, len(s), k):
        yield s[n:(n + k)]


def triplets(s: str):
    yield from kplets(3, s)


def backward(s: str) -> str:
    return s[::-1]


def nnna_to_dict(s: str, n=3, a=1) -> dict:
    """
    Takes a string like
        UUU F UUC F ...
    Returns a dictionary
        {'UUU': 'F', 'UUC': 'F', ...}
    White spaces and new lines are ignored.
    """
    from tcga.utils import First
    f = First(str.split).then(''.join).then(lambda s: kplets(n + a, s)).each(lambda s: (s[0:n], s[n:(n + a)]))
    return dict(f(s))
