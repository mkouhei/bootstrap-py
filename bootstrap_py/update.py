# -*- coding: utf-8 -*-
"""bootstrap_py.update."""
import requests
from defusedxml.ElementTree import fromstring
from bootstrap_py import __version__


class Update(object):
    """bootstrap-py updata checker."""

    badge_url = 'https://img.shields.io/pypi/v/bootstrap-py.svg'
    name_space = '{http://www.w3.org/2000/svg}'

    def __init__(self):
        """Initialize."""
        self.current_version = 'v{0}'.format(__version__)
        self.latest_version = self._latest_version()

    def _latest_version(self):
        try:
            resp = requests.get(self.badge_url)
        except requests.exceptions.ConnectionError:
            return '0.0.0'
        element_tree = fromstring(resp.text)
        return element_tree.findall(
            '{ns}g'.format(ns=self.name_space))[1].findall(
                '{ns}text'.format(ns=self.name_space))[2].text

    def updatable(self):
        """bootstrap-py package updatable?."""
        if self.latest_version > self.current_version:
            return self.latest_version
        else:
            return False

    def show_message(self):
        """Show message updatable."""
        print(
            'current version: {current_version}\n'
            'latest version : {latest_version}'.format(
                current_version=self.current_version,
                latest_version=self.latest_version))
