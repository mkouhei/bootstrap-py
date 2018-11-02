# -*- coding: utf-8 -*-
"""bootstrap_py.tests.stub."""
import requests_mock
from bootstrap_py.classifiers import Classifiers
from bootstrap_py.update import Update


def stub_request_metadata(badge=False):
    """Stub request classifiers, badge."""
    if badge:
        with requests_mock.Mocker() as mock:
            with open('bootstrap_py/tests/data/badge.svg') as fobj:
                svg_data = fobj.read()
                mock.get(Update.badge_url,
                         text=svg_data,
                         status_code=200)

    with requests_mock.Mocker() as mock:
        with open('bootstrap_py/data/classifiers.txt') as fobj:
            data = fobj.read()
            mock.get(Classifiers.url,
                     text=data,
                     status_code=200)
            return Classifiers()
