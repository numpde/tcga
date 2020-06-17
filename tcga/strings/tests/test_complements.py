# RA, 2020-06-17

import unittest


class TestComplements(unittest.TestCase):
    def test_basic(self):
        from tcga.strings.complements import dna_to_dna
        self.assertEqual("CGTA", dna_to_dna("GCAT"))



if __name__ == "__main__":
    # https://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing
    import sys
    import unittest

    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=3).run(suite)
