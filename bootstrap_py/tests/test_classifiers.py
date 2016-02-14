# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_classifiers."""
import unittest
import requests_mock
from bootstrap_py.classifiers import Classifiers


class ClassifiersTests(unittest.TestCase):
    """bootstrap_py.classifiers.Classifiers tests."""

    def setUp(self):
        """Prepare test data."""
        with requests_mock.Mocker() as mock:
            with open('bootstrap_py/data/classifiers.txt') as fobj:
                data = fobj.read()
            mock.get(Classifiers.url,
                     text=data,
                     status_code=200)
            self.data = Classifiers()

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
