# -*- coding: utf-8 -*-
import unittest
import util.sample as sample

class TestUtil(unittest.TestCase):
    def test_print(self) -> None:
        self.assertEqual(sample.Util.print(), 'This is Util')
