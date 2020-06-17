# RA, 2020-06-17

from unittest import TestCase

from tcga.strings import CircularView


class TestCircularView(TestCase):
    @classmethod
    def Circular(cls, s):
        class View:
            def __init__(self, s):
                self.s = s

            def __getitem__(self, v):
                import numpy as np
                if (len(self.s) == 0):
                    return self.s
                s = tuple(self.s)
                C = type(self.s)
                ii = np.arange(v.start, v.stop, v.step)
                if not len(ii):
                    return C()
                while min(ii) < 0:
                    ii += len(s)
                while len(s) <= max(ii):
                    s = s * 2
                if isinstance(self.s, str):
                    return ''.join(np.asarray(s)[ii])
                else:
                    return sum(map(C, np.asarray(s)[ii]), C())

        return View(s)

    def test_step0(self):
        with self.assertRaises(ValueError):
            x = CircularView("ABC")[1:2:0]

    def test_empty(self):
        for S in ["", list(), tuple(), []]:
            for v in [slice(-3, 6, 2), slice(0, 1, 1)]:
                self.assertEqual(self.Circular(S)[v], CircularView(S)[v])

    def test_strings_forward_and_backward(self):
        S = "0123456"

        self.assertEqual(self.Circular(S)[7:-4:-2], "053164")

        v = slice(0, 0, 1)
        self.assertEqual(self.Circular(S)[v], CircularView(S)[v])

        v = slice(-13, 1, 4)
        self.assertEqual(self.Circular(S)[v], CircularView(S)[v])

        v = slice(0, 21, 1)
        self.assertEqual(self.Circular(S)[v], CircularView(S)[v])

        v = slice(-217, 1231, 3)
        self.assertEqual(self.Circular(S)[v], CircularView(S)[v])

        v = slice(-17, -22, -1)
        self.assertEqual(self.Circular(S)[v], CircularView(S)[v])

        for i in range(-17, 11):
            for n in range(-13, 13):
                for s in [-34, -7, -4, -2, -1, None, 1, 2, 3, 4, 5, 97]:
                    v = slice(i, i + n, s)
                    v.indices(1)
                    self.assertEqual(self.Circular(S)[v], CircularView(S)[v])

    def test_list_forward_and_backward(self):
        S = list("0123456")

        v = slice(12, -9, -2)
        self.assertListEqual(self.Circular(S)[v], CircularView(S)[v])

        for i in range(-17, 11):
            for n in range(-13, 13):
                for s in [-34, -7, -4, -2, -1, None, 1, 2, 3, 4, 5, 97]:
                    v = slice(i, i + n, s)
                    v.indices(1)
                    self.assertListEqual(self.Circular(S)[v], CircularView(S)[v])

    def test_tuple(self):
        S = tuple("0123456")
        v = slice(12, -9, -2)
        self.assertTupleEqual(self.Circular(S)[v], CircularView(S)[v])


if __name__ == "__main__":
    # https://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing
    import sys
    import unittest

    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=3).run(suite)
