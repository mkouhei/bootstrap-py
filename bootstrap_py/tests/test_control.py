# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_control."""
import unittest
import os
import tempfile
import shutil
import requests_mock
from bootstrap_py import control, exceptions, pypi
from bootstrap_py.classifiers import Classifiers
from bootstrap_py.tests.test_package import Dummy


class ControlTests(unittest.TestCase):
    """bootstrap_py.control tests."""

    def setUp(self):
        """prepare test data."""
        self.testdir = tempfile.mkdtemp(suffix='-bootstrap-py-test-control')
        self.params = Dummy()
        setattr(self.params, 'name', 'foo')
        setattr(self.params, 'outdir', self.testdir)

    def tearDown(self):
        """clean up."""
        shutil.rmtree(self.testdir)

    def test_retreive_metadata(self):
        """retreive_metadata."""
        with requests_mock.Mocker() as _mock:
            with open('bootstrap_py/data/classifiers.txt') as fobj:
                data = fobj.read()
            _mock.get(Classifiers.url,
                      text=data,
                      status_code=200)
        self.assertTrue(hasattr(control.retreive_metadata(), 'status'))
        self.assertTrue(hasattr(control.retreive_metadata(), 'licenses'))

    def test_check_repository_existence(self):
        """check_repository_existence."""
        # pylint: disable=no-member
        os.makedirs(os.path.join(self.params.outdir, self.params.name))
        with self.assertRaises(exceptions.Conflict):
            control.check_repository_existence(self.params)

    def test_check_package_existence(self):
        """check_package_existence."""
        with requests_mock.Mocker() as _mock:
            _mock.get(pypi.PYPI_URL.format(self.params.name), status_code=200)
            setattr(self.params, 'no_check', False)
            with self.assertRaises(exceptions.Conflict):
                control.check_package_existence(self.params)
