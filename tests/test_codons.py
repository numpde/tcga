# RA, 2020-06-18

from unittest import TestCase
from itertools import product


class TestCodonTables(TestCase):
    def test_sanity(self):
        from tcga.codons import standard_rna as rna_codons
        self.assertEqual(type(rna_codons), dict)
        self.assertEqual(len(rna_codons), 4 ** 3)
        self.assertSetEqual(set(rna_codons.keys()), set(map(''.join, product("ACGU", repeat=3))))
        self.assertSetEqual(set(rna_codons.values()), set("ARNDCQEGHILKMFPSTWYV*"))
