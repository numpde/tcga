# RA, 2020-06-17

import unittest

from tcga.utils import First
from tcga.gencode import rna_codons, triplets
from tcga.strings.complements import dna_to_rna, dna_to_dna, backward


class TestCompose(unittest.TestCase):
    def test_transcription_translation(self):
        f = First(dna_to_dna.reversed).then(dna_to_rna).then(triplets).each(rna_codons).then(''.join)
        self.assertEqual(f(backward("CACGAACTTGTCGAGACCATTGCC")), "HELVETIA")


if __name__ == "__main__":
    # https://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing
    import sys
    import unittest

    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=3).run(suite)
