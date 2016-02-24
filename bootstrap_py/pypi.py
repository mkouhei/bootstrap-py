# -*- coding: utf-8 -*-
"""bootstrap_py.pypi."""
import sys
import socket
from bootstrap_py.exceptions import BackendFailure, Conflict
if sys.version_info < (3, 0):
    import xmlrpclib as xmlrpc_client
else:
    from xmlrpc import client as xmlrpc_client

#: PyPI XML-RPC API url
PYPI_URL = 'https://pypi.python.org/pypi'


def package_existent(name):
    """search package.

    * :class:`bootstrap_py.exceptions.Conflict` exception occurs
      when user specified name has already existed.

    * :class:`bootstrap_py.exceptions.BackendFailure` exception occurs
      when PyPI service is down.

    :param str name: package name
    """
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
    """search package.

    :param str name: package name

    :rtype: list
    :return: package name list
    """
    client = xmlrpc_client.ServerProxy(PYPI_URL)
    return [pkg for pkg in client.search({'name': name})
            if pkg.get('name') == name]
