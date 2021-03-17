# RA, 2021-03-17

import unittest
import io
from tcga.utils import Peek


class TestPeek(unittest.TestCase):
    def test_no_arg(self):
        with Peek():
            pass

    def test_with_arg(self):
        with Peek(print):
            pass

    def test_callable_empty(self):
        with Peek(lambda x: None) as peek:
            peek()

    def test_callable_returns(self):
        with Peek(lambda x: None) as peek:
            self.assertEqual(123, peek(123))

    def test_reports(self):
        s = io.StringIO()
        with Peek(s.write) as peek:
            peek("123")
        self.assertEqual(s.getvalue(), "123")

    def test_doesnt_report(self):
        with Peek() as peek:
            peek("123")
