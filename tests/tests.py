#
from asd import *
import unittest


class TestCase(unittest.TestCase):

    def testAdd(self):
        self.assertEqual(6, add(3, 2))

unittest.main()
