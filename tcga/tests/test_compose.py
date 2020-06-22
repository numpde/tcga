# RA, 2020-06-17

import unittest

from tcga.utils import First
from tcga.codons.tables import standard as codons
from tcga.strings.complements import dna_to_rna, dna_to_dna
from tcga.strings import triplets, backward

class TestCompose(unittest.TestCase):
    def test_transcription_translation(self):
        f = First(dna_to_dna.reverse).then(dna_to_rna).then(triplets).each(codons).join(str)
        self.assertEqual(f(backward("CACGAACTTGTCGAGACCATTGCC")), "HELVETIA")

