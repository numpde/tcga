# RA, 2020-06-17

import unittest

from tcga.utils import First
from tcga.codons import standard_rna as codons
from tcga.complements.complements import dna_to_rna, dna_to_dna
from tcga.strings import triplets, reverse


class TestFirst(unittest.TestCase):
    def test_composition1(self):
        f = First(dna_to_dna.reverse).then(dna_to_rna).then(triplets).each(codons).join(str)
        self.assertEqual(f(reverse("CACGAACTTGTCGAGACCATTGCC")), "HELVETIA")

    def test_keep1(self):
        f = First(sorted).keep(lambda x: (x > 2)).then(list)
        self.assertListEqual(f([4, 3, 2, 1, 5]), [3, 4, 5])

    def test_keep2(self):
        f = First(sorted).keep().then(list)
        self.assertListEqual(f([2, 1, 3, 0]), [1, 2, 3])

    def test_keep3(self):
        f = First(sorted).keep().then(list)
        self.assertListEqual(f([True, False]), [True])
