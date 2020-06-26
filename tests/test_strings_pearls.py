# RA, 2020-06-18

from unittest import TestCase
import tcga.strings.pearls as pearls


class Backward(TestCase):
    def test_str(self):
        self.assertEqual("", pearls.reverse(""))
        self.assertEqual("4321", pearls.reverse("1234"))

    def test_tuple(self):
        self.assertEqual(tuple("4321"), pearls.reverse(tuple("1234")))


class Triplets(TestCase):
    def test_type(self):
        from types import GeneratorType
        self.assertIsInstance(pearls.triplets("123"), GeneratorType)

    def test_ok(self):
        self.assertListEqual(["123", "456"], list(pearls.triplets("123456")))

    def test_fail(self):
        with self.assertRaises(ValueError):
            list(pearls.triplets("1234567"))


class NNNA(TestCase):
    def test_dictable(self):
        dict(pearls.nnna("1234"))

    def test_ok(self):
        self.assertDictEqual(dict(pearls.nnna(" A  B \n C D \n a  b c  d  ")), {'ABC': "D", 'abc': "d"})

    def test_fail(self):
        with self.assertRaises(ValueError):
            list(pearls.nnna("12345"))

