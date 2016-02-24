# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_control."""
import unittest
import requests_mock
from bootstrap_py import control
from bootstrap_py.classifiers import Classifiers


class ControlTests(unittest.TestCase):
    """bootstrap_py.control tests."""

    def test_retreive_metadata(self):
        """retreive_metadata."""
        with requests_mock.Mocker() as mock:
            with open('bootstrap_py/data/classifiers.txt') as fobj:
                data = fobj.read()
            mock.get(Classifiers.url,
                     text=data,
                     status_code=200)
        self.assertTrue(hasattr(control.retreive_metadata(), 'status'))
        self.assertTrue(hasattr(control.retreive_metadata(), 'licenses'))
