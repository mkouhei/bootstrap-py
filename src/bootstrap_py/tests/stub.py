# -*- coding: utf-8 -*-
"""bootstrap_py.tests.stub."""
import os
import requests_mock
from pathlib import Path
from bootstrap_py.classifiers import Classifiers
from bootstrap_py.update import Update


def stub_request_metadata(badge=False):
    """Stub request classifiers, badge."""
    if badge:
        with requests_mock.Mocker() as mock:
            badge_path = os.path.join(
                Path(__file__).parents[0],
                'data/badge.svg'
            )
            with open(badge_path) as fobj:
                svg_data = fobj.read()
                mock.get(Update.badge_url,
                         text=svg_data,
                         status_code=200)

    with requests_mock.Mocker() as mock:
        classifiers_path = os.path.join(
            Path(__file__).parents[2],
            'bootstrap_py/data/classifiers.txt'
        )
        with open(classifiers_path) as fobj:
            data = fobj.read()
            mock.get(Classifiers.url,
                     text=data,
                     status_code=200)
            return Classifiers()
