# RA, 2020-06-19

import json
from tcga.data import aaindex

pretty = (lambda x: json.dumps(dict(x), indent=2, default=(lambda x: '...')))

print("AAindex objects (excerpts):")
print("indices =   ", pretty(aaindex.indices.head(3)))
print("matrices =  ", pretty(aaindex.matrices.head(3)))
print("potentials =", pretty(aaindex.potentials.head(3)))

print("-" * 42)

key = 'ALTS910101'
print(F"Record for '{key}' =", pretty(aaindex.data[key]))
print("where the matrix M is:")
print(aaindex.data[key]['M'])
