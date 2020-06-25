# RA, 2020-06-25

import json
pretty = (lambda x: json.dumps(dict(x), indent=2, default=(lambda x: '...')))

print("[BLOSUM62 -- AAindex]")
from tcga.data.aaindex import data
i = 'HENS920102'  # ID of BLOSUM62
A = data[i].M
print(data[i].D, data[i]['*'], sep='\n')
print("Matrix:", A.astype(int).head(3), "...", sep='\n')

print("[BLOSUM62 -- FASTA]")
from tcga.data.blosum import blosum62_12 as B
from tcga.refs import annotations
print(pretty(annotations[B]), sep="\n")
print("Matrix:", B.head(3), "...", sep='\n')
