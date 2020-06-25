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

    def test_same_as_aaindex(self):
        import tcga.data.blosum as B
        import tcga.data.aaindex as A
        I = {'HENS920101': B.blosum45, 'HENS920104': B.blosum50, 'HENS920102': B.blosum62, 'HENS920103': B.blosum80}
        for (i, X) in I.items():
            Y = A.data[i].M
            X = X.loc[Y.index, Y.columns]  # X is a superset of Y
            diff = (X - Y).abs().sum().sum()
            if (i == 'HENS920102'):
                # BLOSUM62 matrices do not match
                # One is 1/2 bit units, the other is 1/3 bit units
                self.assertEqual(diff, 388)
            else:
                self.assertEqual(diff, 0, )
