# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_control."""
import unittest
from datetime import datetime
from bootstrap_py import control


# pylint: disable=too-few-public-methods
class Dummy(object):
    """Dummy class."""
    pass


class PackageDataTests(unittest.TestCase):
    """bootstrap_py.control.PackageData tests."""

    def setUp(self):
        """Prepare test data."""
        self.params = Dummy()
        setattr(self.params, 'foo', 'hoge')
        setattr(self.params, 'bar', 'moge')
        setattr(self.params, 'baz', 'fuga')

        self.default_params = Dummy()
        setattr(self.default_params, 'date', '2016-01-29')
        setattr(self.default_params, 'version', '1.0.0')
        setattr(self.default_params, 'description', 'dummy description.')

    def test_provides_paras(self):
        """provides params without default params."""
        # pylint: disable=no-member
        pkg_data = control.PackageData(self.params)
        self.assertEqual(pkg_data.foo, 'hoge')
        self.assertEqual(pkg_data.bar, 'moge')
        self.assertEqual(pkg_data.baz, 'fuga')
        self.assertEqual(pkg_data.date, datetime.utcnow().strftime('%Y-%m-%d'))
        self.assertEqual(pkg_data.version, '0.1.0')
        self.assertEqual(pkg_data.description, '##### ToDo: Rewrite me #####')

    def test_provides_default_params(self):
        """provides params without default params."""
        # pylint: disable=no-member
        pkg_data = control.PackageData(self.default_params)
        self.assertEqual(pkg_data.date, '2016-01-29')
        self.assertEqual(pkg_data.version, '1.0.0')
        self.assertEqual(pkg_data.description, 'dummy description.')

    def test_convert_to_dict(self):
        """convert PackageData to dict."""
        dict_data = control.PackageData(self.default_params).to_dict()
        self.assertDictEqual(dict_data,
                             {'date': '2016-01-29',
                              'version': '1.0.0',
                              'description': 'dummy description.'})
