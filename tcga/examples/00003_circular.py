# RA, 2020-06-18

from tcga.strings import Circular
# This creates a circular view onto the string
c = Circular("ABCDEFG")
print(F"c = {c}", c[0:20], c[-3:20:2], type(c[0:20]), sep=', ')

from tcga.strings import laola
# This this looks at a str/list/tuple in a circular way
v = laola[-3:20:2]
print(v("ABCDEFG"))
