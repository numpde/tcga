# RA, 2020-06-19

import json
from tcga.data import aaindex
from tcga.refs import annotations

pretty = (lambda x: json.dumps(dict(x), indent=2, default=(lambda x: '...')))

print("AAindex objects (excerpts):")
print("indices", pretty(aaindex.indices.head(3)), sep=" = ")
print("matrices", pretty(aaindex.matrices.head(3)), sep=" = ")
print("potentials", pretty(aaindex.potentials.head(3)), sep=" = ")

print("-" * 42)

key = 'ALTS910101'
print(F"Record for '{key}'", pretty(aaindex.data[key]), sep=" = ")
print("where the matrix M is:")
print(aaindex.data[key]['M'])

print("-" * 42)

print("Source:")
print(annotations[aaindex.data]['source'])
