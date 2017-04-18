# -*- coding: utf-8 -*-
"""bootstrap_py.exceptions."""


class Error(Exception):
    """Base error class."""

    pass


class NotFound(Error):
    """Not Found."""

    pass


class Conflict(Error):
    """Confilict."""

    pass


class BackendFailure(Error):
    """PyPI service down."""

    pass
