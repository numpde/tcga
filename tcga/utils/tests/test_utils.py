# RA, 2020-06-17


from unittest import TestCase


class TestFirst(TestCase):
    def test_construct(self):
        from tcga.utils import First
        f = (lambda x: x * 2)
        First(f)

    def test_func_composition(self):
        from tcga.utils import First
        f = (lambda x: x * 2)
        g = (lambda y: y - 1)
        h = (lambda z: z ** 2)
        self.assertEqual(First(f).then(g)(2), g(f(2)))
        self.assertEqual(First(f).then(g).then(h)[2], h(g(f(2))))

        self.assertEqual(First(str.upper)["AbC"], "ABC")
        self.assertEqual(First(str.strip).then(str.lower)[" AbC "], "abc")
        self.assertEqual(First(str.lower).then(str.strip)[" AbC "], "abc")
        self.assertEqual(First(list.pop).then(str.lower).then(tuple)(["ABC", "XYZ"]), ('x', 'y', 'z'))

    def test_mul(self):
        from tcga.utils import First as F
        f = (lambda x: x * 2)
        g = (lambda y: y - 1)
        X = F(f) @ F(g)
        self.assertEqual(X(11), f(g(11)))

    def test_dict_composition(self):
        from tcga.utils import First
        f = (lambda x: x * 2)
        g = {2: 3}
        h = {3: 4}
        self.assertEqual(First(f).then(g).then(h)(1), 4)

    def test_noncomposable(self):
        from tcga.utils import First
        with self.assertRaises(RuntimeError):
            First(1)
        with self.assertRaises(RuntimeError):
            First(lambda x: x).then(2)


if __name__ == "__main__":
    # https://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing
    import sys
    import unittest

    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=3).run(suite)
