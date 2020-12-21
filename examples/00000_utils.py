import io
from pathlib import Path

from tcga.utils import unlist1
# Returns the object from a list
# iff the list is a singleton
assert 43 == unlist1([43])
# An iterable will be consumed:
assert 36 == unlist1((x ** 2) for x in [6])
# These fail with a ValueError:
# unlist1([])
# unlist1([1, 2])

from tcga.utils import relpath
# Returns the path relative to the script

from tcga.utils import mkdir
# A wrapper for Path.mkdir:
# path = mkdir(Path("/path/to/folder"))

from tcga.utils import first
# Returns the first element of an iterable
assert 'A' == first("ABCD")

from tcga.utils import at_most_n
# Lazy cut-off for iterables
print(list(at_most_n("ABCD", n=2)))
# ['A', 'B']

from tcga.utils import whatsmyname
def rose():
    print(whatsmyname())
    # Prints the name of
    # the function: rose

from tcga.utils import assert_exists
# If `file` is a filename or path then
#   assert_exists(file)
# either raises FileNotFoundError
# or returns back `file`

from tcga.utils import md5
# Computes the md5 hash of a text stream chunkwise.
# Attempts to rewind the stream back using .tell()
print(md5(io.StringIO("I know that I shall meet my fate")))
# 06a118b2f090ed1b39a1d07efdaa5d78

from tcga.utils import from_iterable
# Wraps chain.from_iterable, i.e.
print(set(from_iterable([[1, 2, 5], [4, 5]])))
print(from_iterable([[1, 2, 5], [4, 5]], type=set))
# {1, 2, 4, 5}

from tcga.utils import minidict
# A minimalistic read-only dictionary
minidict({1: 'A', 2: 'B'})

from tcga.utils import seek_then_rewind
# Context manager for rewinding file descriptors
with open(__file__, mode='r') as fd:
    with seek_then_rewind(fd, seek=2):
        print(fd.readline().strip())
        # port io
    print(fd.readline().strip())
    # import io
