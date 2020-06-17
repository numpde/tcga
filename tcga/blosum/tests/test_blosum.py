# RA, 2020-06-17


from unittest import TestCase


class TestFirst(TestCase):
    def test_type_and_symmetry(self):
        import pandas as pd
        from tcga.blosum import blosum45 as A, blosum50 as B, blosum62 as C, blosum80 as D
        for M in [A, B, C, D]:
            self.assertIsInstance(M, pd.DataFrame)
            self.assertTrue(M.equals(M.T))


if __name__ == "__main__":
    # https://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing
    import sys
    import unittest

    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=3).run(suite)
