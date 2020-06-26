# RA, 2020-06-18

from unittest import TestCase
from tcga.refs import annotations


def members(mod):
    import inspect
    return [b for (a, b) in inspect.getmembers(mod) if not a.startswith("_") and not inspect.ismodule(b)]


class TestAnnotationsPresent(TestCase):
    def test_data_aaindex(self):
        import tcga.data.aaindex as tables
        for T in members(tables):
            self.assertIn(T, annotations)
            self.assertIn('source', annotations[T])

    def test_data_sa(self):
        import tcga.data.sa_aa_ref_chart as tables
        for T in members(tables):
            self.assertIn(T, annotations)
            self.assertIn('source', annotations[T])

    def test_data_blosum(self):
        import tcga.data.blosum as tables
        for T in members(tables):
            self.assertIn(T, annotations)
            self.assertIn('source', annotations[T])

    def test_codons(self):
        import tcga.codons as tables
        for T in members(tables):
            self.assertIn(T, annotations)
            self.assertIn('source', annotations[T])
