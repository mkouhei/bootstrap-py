# -*- coding: utf-8 -*-
"""bootstrap_py.classifiers."""
import re
import requests


class Classifiers(object):
    """Classifiers."""

    url = 'https://pypi.python.org/pypi?%3Aaction=list_classifiers'
    prefix_status = 'Development Status :: '
    prefix_lic = 'License :: OSI Approved :: '

    def __init__(self):
        """Initialize."""
        self.resp = requests.get(self.url)

    def status(self):
        """Development status."""
        return {self._acronym_status(l): l for l in self.resp.text.split('\n')
                if l.startswith(self.prefix_status)}

    @staticmethod
    def _acronym_status(status_statement):
        """convert development status acronym."""
        return status_statement.split(' - ')[1]

    def licenses(self):
        """OSI Approved license."""
        return {self._acronym_lic(l): l for l in self.resp.text.split('\n')
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
