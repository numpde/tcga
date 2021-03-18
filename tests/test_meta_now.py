# RA, 2021-03-18

import unittest
from tcga.utils import Now


class TestNow(unittest.TestCase):
    def test_construct(self):
        Now()

    def test_str(self):
        now = Now()
        self.assertEqual(str(now), now.t.strftime("%Z-%Y%m%d-%H%M%S"))

    def test_utc(self):
        now = Now()
        self.assertEqual(now.utc_iso, now.t.isoformat(sep=' ', timespec='seconds'))

    def test_utc_ms(self):
        now = Now()
        self.assertEqual(now.utc_iso_ms, now.t.isoformat(sep=' ', timespec='microseconds'))

    def test_utc_sep(self):
        sep = 'X'
        now = Now(sep=sep)
        self.assertEqual(now.utc_iso, now.t.isoformat(sep=sep, timespec='seconds'))

    def test_utc_ms_sep(self):
        sep = 'X'
        now = Now(sep=sep)
        self.assertEqual(now.utc_iso_ms, now.t.isoformat(sep=sep, timespec='microseconds'))
