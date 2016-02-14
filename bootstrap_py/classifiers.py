# -*- coding: utf-8 -*-
"""bootstrap_py.classifiers."""
import os
import re
import requests
from bootstrap_py import __file__

# See: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings()


class Classifiers(object):
    """Classifiers."""

    url = 'https://pypi.python.org/pypi?%3Aaction=list_classifiers'
    prefix_status = 'Development Status :: '
    prefix_lic = 'License :: OSI Approved :: '
    timeout = 5.000

    def __init__(self):
        """Initialize."""
        try:
            self.resp_text = requests.get(self.url, timeout=self.timeout).text
        except requests.exceptions.ConnectionError:
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     'data/classifiers.txt'))
            with open(file_path) as fobj:
                self.resp_text = fobj.read()

    def status(self):
        """Development status."""
        return {self._acronym_status(l): l for l in self.resp_text.split('\n')
                if l.startswith(self.prefix_status)}

    @staticmethod
    def _acronym_status(status_statement):
        """convert development status acronym."""
        return status_statement.split(' - ')[1]

    def licenses(self):
        """OSI Approved license."""
        return {self._acronym_lic(l): l for l in self.resp_text.split('\n')
                if l.startswith(self.prefix_lic)}

    def licenses_desc(self):
        """removed prefix."""
        return {self._acronym_lic(l): l.split(self.prefix_lic)[1]
                for l in self.resp_text.split('\n')
                if l.startswith(self.prefix_lic)}

    def _acronym_lic(self, license_statement):
        """convert license acronym."""
        pat = re.compile(r'\(([\w+\W?\s?]+)\)')
        if pat.search(license_statement):
            lic = pat.search(license_statement).group(1)
            if lic.startswith('CNRI'):
                return lic[:4]
            else:
                return lic.replace(' ', '')
        else:
            return ''.join(
                [w[0]
                 for w in license_statement.split(self.prefix_lic)[1].split()])
