# RA, 2020-06-18

from unittest import TestCase


class TestReferences(TestCase):
    def test_alive(self):
        from tcga.refs import annotations
        ref = {'author': "anon"}
        annotations[self] = ref
        self.assertIn(self, annotations)
        self.assertDictEqual(annotations[self], ref)

    def test_default(self):
        from tcga.refs import annotations
        ref = {'author': "anon"}
        annotations[self]['author'] = ref['author']
        self.assertDictEqual(annotations[self], ref)

    def test_raises(self):
        from tcga.refs import annotations

        with self.assertRaises(ValueError):
            annotations[self] = "123"

        annotations[self] = {'author': "anon"}
        with self.assertRaises(KeyError):
            annotations[self] = {}

