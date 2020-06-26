# RA, 2020-06-17

from tcga.codons import standard_rna
print("RNA codons (standard):", standard_rna, sep='\n')
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
