# RA, 2020-06-17

from tcga.codons import standard_rna
print("RNA codons (standard):")
print(standard_rna)
# {'UUU': 'F', 'UUC': 'F', 'UUA': 'L', ...}

from tcga.codons import tables
print("Other codon tables:")
print(tables.name)
# 1: Standard, 2: Vertebrate Mitochondrial, 3: Yeast Mitochondrial ...

print("For example:")
print(tables.loc[1])
# name                                                   Standard
# short_name                                                 SGC0
# dna_codons    {'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L...
# rna_codons    {'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L...

# Those are the same
assert tables.rna_codons[1] == standard_rna

import json
from tcga.refs import annotations
print(json.dumps(annotations[tables], indent=2))
# {
#   "comments": [
#     "Compiled from the NCBI list of genetic codes.",
#     "https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi"
#   ],
#   "datetime": "2020-06-26 16:07:16.284170+00:00",
#   "source": {
#     "source": "ftp://ftp.ncbi.nih.gov/entrez/misc/data/gc.prt",
#     "datetime": "2020-06-26 14:38:28.600903+00:00"
#   }
# }
