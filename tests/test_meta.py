# RA, 2021-03-19

import unittest
from tcga.utils import whatsmyname, this_module_body


class TestInspect(unittest.TestCase):
    def test_whatsmyname(self):
        self.assertEqual("test_whatsmyname", whatsmyname())

    def test_this_module_body(self):
        self.assertTrue(this_module_body().strip().endswith("# do not remove or modify this line"))


# do not remove or modify this line
