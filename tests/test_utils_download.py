# RA, 2020-06-26

from unittest import TestCase
from tcga.utils import download
from tempfile import TemporaryDirectory
from urllib.error import URLError
from pathlib import Path


class TestDownload(TestCase):
    def test_silent_accept_bad_url(self):
        x = download("-")

    def test_fail_no_to(self):
        with self.assertRaises(RuntimeError):
            x = download("-").now

    def test_rel_or_abs(self):
        with self.assertRaises(RuntimeError):
            download("-").to(rel_path="cache", abs_path="cache")
        with self.assertRaises(TypeError):
            download("-").to("cache")

    def test_fail_bad_url(self):
        with TemporaryDirectory() as tempdir:
            with self.assertRaises(ValueError):
                x = download("-").to(abs_path=tempdir).now
            with self.assertRaises(URLError):
                x = download("http://").to(abs_path=tempdir).now

    def test_makes_folder(self):
        with TemporaryDirectory() as tempdir:
            folder = Path(tempdir) / "test"
            with self.assertRaises(ValueError):
                x = download("-").to(abs_path=folder).now
            self.assertTrue(folder.exists())
        self.assertTrue(not folder.exists())

    def test(self):
        pass
