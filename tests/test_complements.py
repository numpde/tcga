# RA, 2020-06-17

import unittest


class TestComplements(unittest.TestCase):
    def test_basic(self):
        from tcga.complements.complements import dna_to_dna
        self.assertEqual("CGTA", dna_to_dna("GCAT"))


