# RA, 2020-06-17


from unittest import TestCase


class TestFirst(TestCase):
    def test_type_and_symmetry(self):
        import pandas as pd
        from tcga.data.blosum import blosum45 as A, blosum50 as B, blosum62 as C, blosum80 as D
        for M in [A, B, C, D]:
            self.assertIsInstance(M, pd.DataFrame)
            self.assertTrue(M.equals(M.T))

    def test_annotation(self):
        from tcga.data.blosum import blosum45 as A, blosum50 as B, blosum62 as C, blosum80 as D
        from tcga.refs import annotations
        for M in [A, B, C, D]:
            self.assertIn(M, annotations)
            self.assertIn('source', annotations[M])
