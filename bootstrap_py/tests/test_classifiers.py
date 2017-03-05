# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_classifiers."""
import unittest
from bootstrap_py.classifiers import Classifiers
from bootstrap_py.tests.stub import stub_request_metadata


class ClassifiersTests(unittest.TestCase):
    """bootstrap_py.classifiers.Classifiers tests."""

    def setUp(self):
        """Prepare test data."""
        self.data = stub_request_metadata()

    def test_status(self):
        """respond dict status."""
        self.assertEqual(len(self.data.status().keys()), 7)
        self.assertEqual(len(self.data.status().values()), 7)

    def test_licenses(self):
        """respond dict licenses."""
        self.assertEqual(len(self.data.licenses().keys()), 49)
        self.assertEqual(len(self.data.licenses().values()), 49)

    def test_licenses_desc(self):
        """respond dic licenses description."""
        self.assertEqual(len(self.data.licenses_desc().keys()), 49)
        self.assertEqual(len(self.data.licenses_desc().values()), 49)
        for val in self.data.licenses_desc().values():
            self.assertTrue(Classifiers.prefix_lic not in val)
