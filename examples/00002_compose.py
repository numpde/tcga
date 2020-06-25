# RA, 2020-06-18

from tcga.utils import First
from tcga.codons.tables import standard as rna_codons
from tcga.complements import dna_to_rna, dna_to_dna
from tcga.strings import triplets, reverse

X = reverse("CACGAACTTGTCGAGACCATTGCC")

f = First(dna_to_dna.reverse).then(dna_to_rna).then(triplets).each(rna_codons).join(str)
print(X, "=>", f(X))
