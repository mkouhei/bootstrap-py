# -*- coding: utf-8 -*-
"""bootstrap_py.pypi."""
import requests
import socket
from requests.exceptions import Timeout, HTTPError
from bootstrap_py.exceptions import BackendFailure, Conflict

#: PyPI JSONC API url
PYPI_URL = 'https://pypi.org/pypi/{0}/json'


def package_existent(name):
    """Search package.

    * :class:`bootstrap_py.exceptions.Conflict` exception occurs
      when user specified name has already existed.

    * :class:`bootstrap_py.exceptions.BackendFailure` exception occurs
      when PyPI service is down.

    :param str name: package name
    """
    try:
        response = requests.get(PYPI_URL.format(name))
        if response.ok:
            msg = ('[error] "{0}" is registered already in PyPI.\n'
                   '\tSpecify another package name.').format(name)
            raise Conflict(msg)
    except (socket.gaierror,
            Timeout,
            ConnectionError,
            HTTPError) as exc:
        raise BackendFailure(exc) from exc
