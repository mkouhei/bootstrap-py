# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_pypi."""
import unittest
import json
import sys
import socket
import mock
from bootstrap_py import pypi, exceptions
if sys.version_info < (3, 0):
    import xmlrpclib as xmlrpc_client
else:
    from xmlrpc import client as xmlrpc_client


def search_result():
    """dummy result."""
    with open('bootstrap_py/tests/data/search_result') as fobj:
        return [json.loads(fobj.read())[8]]


class PyPITests(unittest.TestCase):
    """bootstrap_py.pypi tests."""

    if sys.version_info < (3, 0):
        @mock.patch('xmlrpclib.ServerProxy')
        def test_search_package(self, _mock):
            """search package for Python2."""
            client_mock = _mock.return_value
            client_mock.search.return_value = search_result()
            self.assertListEqual(pypi.search_package('py-deps'),
                                 search_result())
    else:
        @mock.patch('xmlrpc.client.ServerProxy')
        def test_search_package(self, _mock):
            """search package for Python3."""
            client_mock = _mock.return_value
            client_mock.search.return_value = search_result()
            self.assertListEqual(pypi.search_package('py-deps'),
                                 search_result())

    @mock.patch('bootstrap_py.pypi.search_package')
    def test_package_existent(self, _mock):
        """checking package existent."""
        _mock.return_value = [{'name': 'py-deps'}]
        with self.assertRaises(exceptions.Conflict):
            pypi.package_existent('py-deps')

    @mock.patch('bootstrap_py.pypi.search_package')
    def test_package_existent_duplicate(self, _mock):
        """checking package existent, but this case does not occur."""
        _mock.return_value = [{'name': 'py-deps'},
                              {'name': 'py-deps-dummy'}]
        with self.assertRaises(exceptions.Conflict):
            pypi.package_existent('py-deps')

    @mock.patch('bootstrap_py.pypi.search_package')
    def test_pypi_slow_response(self, _mock):
        """pypi slow response."""
        if sys.version_info < (3, 0):
            # pylint: disable=undefined-variable
            _mock.side_effect = socket.error
        else:
            # pylint: disable=undefined-variable
            _mock.side_effect = TimeoutError
        with self.assertRaises(exceptions.BackendFailure):
            pypi.package_existent('py-deps')

    @mock.patch('bootstrap_py.pypi.search_package')
    def test_pypi_internal_server_down(self, _mock):
        """pypi internal server down."""
        if sys.version_info < (3, 0):
            # pylint: disable=undefined-variable
            _mock.side_effect = socket.error
        else:
            # pylint: disable=undefined-variable
            _mock.side_effect = ConnectionRefusedError
        with self.assertRaises(exceptions.BackendFailure):
            pypi.package_existent('py-deps')

    @mock.patch('bootstrap_py.pypi.search_package')
    def test_pypi_interface_down(self, _mock):
        """pypi interface down."""
        # pylint: disable=undefined-variable
        _mock.side_effect = socket.gaierror
        with self.assertRaises(exceptions.BackendFailure):
            pypi.package_existent('py-deps')

    @mock.patch('bootstrap_py.pypi.search_package')
    def test_pypi_protocol_error(self, _mock):
        """pypi protocol error."""
        _mock.side_effect = xmlrpc_client.ProtocolError(pypi.PYPI_URL,
                                                        400,
                                                        'dummy',
                                                        {})
        with self.assertRaises(exceptions.BackendFailure):
            pypi.package_existent('py-deps')
