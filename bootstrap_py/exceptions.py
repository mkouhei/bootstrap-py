# -*- coding: utf-8 -*-
"""bootstrap_py.exceptions."""


class Error(Exception):
    """Base error class."""

    def __init__(self, message=None):
        """Initialize."""
        super(Error, self).__init__(message)


class NotFound(Error):
    """Not Found."""

    pass


class Conflict(Error):
    """Confilict."""

    pass


class BackendFailure(Error):
    """PyPI service down."""

    pass
