# RA, 2020-06-17

import unittest

from tcga.utils import First
from tcga.codons import standard_rna as codons
from tcga.complements.complements import dna_to_rna, dna_to_dna
from tcga.strings import triplets, reverse

class TestCompose(unittest.TestCase):
    def test_transcription_translation(self):
        f = First(dna_to_dna.reverse).then(dna_to_rna).then(triplets).each(codons).join(str)
        self.assertEqual(f(reverse("CACGAACTTGTCGAGACCATTGCC")), "HELVETIA")

