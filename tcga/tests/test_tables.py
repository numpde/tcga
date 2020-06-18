# RA, 2020-06-18

import unittest
from itertools import product


class TestTables(unittest.TestCase):
    def test_sanity(self):
        from tcga.codons.tables import standard
        self.assertEqual(type(standard), dict)
        self.assertEqual(len(standard), 4 ** 3)
        self.assertSetEqual(set(standard.keys()), set(map(''.join, product("ACGU", repeat=3))))
        self.assertSetEqual(set(standard.values()), set("ARNDCQEGHILKMFPSTWYV*"))

    def test_annotation(self):
        import tcga.codons.tables as tables
        import inspect
        tables = [b for (a, b) in inspect.getmembers(tables) if not a.startswith("__") and not inspect.ismodule(b)]
        from tcga.refs import annotations
        for T in tables:
            self.assertIn(T, annotations)
            self.assertIn('source', annotations[T])
