# -*- coding: utf-8 -*-
"""bootstrap_py.exceptions."""


class Error(Exception):
    """Base error class."""


class NotFound(Error):
    """Not Found."""


class Conflict(Error):
    """Confilict."""


class BackendFailure(Error):
    """PyPI service down."""
