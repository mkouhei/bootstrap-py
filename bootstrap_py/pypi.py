# -*- coding: utf-8 -*-
"""bootstrap_py.pypi."""
import sys
import socket
from bootstrap_py.exceptions import BackendFailure, Conflict
if sys.version_info < (3, 0):
    import xmlrpclib as xmlrpc_client
else:
    from xmlrpc import client as xmlrpc_client


PYPI_URL = 'https://pypi.python.org/pypi'


def package_existent(name):
    """search package."""
    if sys.version_info < (3, 0):
        try:
            result = search_package(name)
        except (socket.error,
                xmlrpc_client.ProtocolError) as exc:
            raise BackendFailure(exc)
    else:
        try:
            result = search_package(name)
        except (socket.gaierror,
                TimeoutError,
                ConnectionRefusedError,
                xmlrpc_client.ProtocolError) as exc:
            raise BackendFailure(exc)
    if len(result):
        msg = ('[error] "{0}" is registered already in PyPI.\n'
               '\tSpecify another package name.').format(name)
        raise Conflict(msg)


def search_package(name):
    """search package."""
    client = xmlrpc_client.ServerProxy(PYPI_URL)
    return [pkg for pkg in client.search({'name': name})
            if pkg.get('name') == name]
