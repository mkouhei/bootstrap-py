# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_pypi."""
import unittest
import json
import mock
import requests
import socket
import requests_mock
from bootstrap_py import pypi, exceptions


def search_result():
    """dummy result."""
    with open('bootstrap_py/tests/data/search_result') as fobj:
        return [json.loads(fobj.read())[8]]


class PyPITests(unittest.TestCase):
    """bootstrap_py.pypi tests."""

    def test_package_existent(self):
        """checking package existent."""
        package_name = 'py-deps'
        with requests_mock.Mocker() as _mock:
            _mock.get(pypi.PYPI_URL.format(package_name), status_code=404)
            self.assertEqual(pypi.package_existent(package_name), None)

    def test_package_existent_duplicate(self):
        """checking package existent, but this case does not occur."""
        package_name = 'py-deps'
        with requests_mock.Mocker() as _mock:
            _mock.get(pypi.PYPI_URL.format(package_name), status_code=200)
            with self.assertRaises(exceptions.Conflict):
                pypi.package_existent(package_name)

    @mock.patch('requests.get')
    def test_pypi_slow_response(self, _mock):
        """pypi slow response."""
        # pylint: disable=undefined-variable
        _mock.side_effect = requests.exceptions.Timeout
        with self.assertRaises(exceptions.BackendFailure):
            pypi.package_existent('py-deps')

    @mock.patch('requests.get')
    def test_pypi_internal_server_down(self, _mock):
        """pypi internal server down."""
        # pylint: disable=undefined-variable
        _mock.side_effect = ConnectionError
        with self.assertRaises(exceptions.BackendFailure):
            pypi.package_existent('py-deps')

    @mock.patch('requests.get')
    def test_pypi_interface_down(self, _mock):
        """pypi interface down."""
        # pylint: disable=undefined-variable
        _mock.side_effect = socket.gaierror
        with self.assertRaises(exceptions.BackendFailure):
            pypi.package_existent('py-deps')

    @mock.patch('requests.get')
    def test_pypi_http_error(self, _mock):
        """pypi http error."""
        _mock.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(exceptions.BackendFailure):
            pypi.package_existent('py-deps')
