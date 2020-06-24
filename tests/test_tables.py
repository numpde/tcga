# RA, 2020-06-18

from unittest import TestCase
from itertools import product
from tcga.refs import annotations


def members(mod):
    import inspect
    return [b for (a, b) in inspect.getmembers(mod) if not a.startswith("_") and not inspect.ismodule(b)]


class TestCodonTables(TestCase):
    def test_sanity(self):
        from tcga.codons.tables import standard
        self.assertEqual(type(standard), dict)
        self.assertEqual(len(standard), 4 ** 3)
        self.assertSetEqual(set(standard.keys()), set(map(''.join, product("ACGU", repeat=3))))
        self.assertSetEqual(set(standard.values()), set("ARNDCQEGHILKMFPSTWYV*"))

    def test_annotation(self):
        import tcga.codons.tables as tables
        for T in members(tables):
            self.assertIn(T, annotations)
            self.assertIn('source', annotations[T])


class TestSAAA(TestCase):
    def test_annotation(self):
        import tcga.data.sa_aa_ref_chart.tables as tables
        for T in members(tables):
            self.assertIn(T, annotations)
            self.assertIn('source', annotations[T])
