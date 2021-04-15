# RA, 2021-03-19

import io
import unittest
import contextlib
from tcga.utils import Section


class TestSection(unittest.TestCase):
    def test_sanity_noarg(self):
        with Section():
            pass

    def test_sanity_desc(self):
        with Section("My section"):
            pass

    def test_desc_print(self):
        s = io.StringIO()
        with contextlib.redirect_stdout(s):
            with Section("My section", print):
                pass
        self.assertTrue(s.getvalue().startswith("test_desc_print"))

