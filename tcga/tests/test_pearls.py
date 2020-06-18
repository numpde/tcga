# RA, 2020-06-18

from unittest import TestCase
import tcga.strings.pearls as pearls


class Backward(TestCase):
    def test_str(self):
        self.assertEqual("", pearls.backward(""))
        self.assertEqual("4321", pearls.backward("1234"))

    def test_tuple(self):
        self.assertEqual(tuple("4321"), pearls.backward(tuple("1234")))


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
    def test_type(self):
        self.assertIs(type(pearls.nnna_to_dict("1234")), dict)

    def test_ok(self):
        self.assertDictEqual(pearls.nnna_to_dict(" A  B \n C D \n a  b c  d  "), {'ABC': "D", 'abc': "d"})

    def test_fail(self):
        with self.assertRaises(ValueError):
            pearls.nnna_to_dict("12345")
