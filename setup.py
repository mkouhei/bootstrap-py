# -*- coding: utf-8 -*-
"""
Copyright (C) 2016 Kouhei Maeda <mkouhei@palmtb.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
from bootstrap_py import __prog__, __version__


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def read_content(filepath):
    with open(filepath) as fobj:
        return fobj.read()


classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: "
    "GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development",
    "Topic :: System :: Archiving :: Packaging",
    "Topic :: System :: Software Distribution",
]


long_description = (
    read_content("README.rst") +
    read_content(os.path.join("docs/source", "CHANGELOG.rst")))

requires = ['setuptools',
            'Jinja2',
            'Sphinx',
            'requests',
            'defusedxml',
            'pguard',
            'GitPython']
extras_require = {
    'reST': ['Sphinx'],
    }
if os.environ.get('READTHEDOCS', None):
    extras_require['reST'].append('recommonmark')

with open('requirements.txt', 'w') as _file:
    _file.write('\n'.join(requires))

with open('extras_requirement.txt', 'w') as _file:
    _file.write('\n'.join(extras_require.get('reST')))

setup(name=__prog__,
      version=__version__,
      description='Bootstrap Python package',
      long_description=long_description,
      author='Kouhei Maeda',
      author_email='mkouhei@palmtb.net',
      url='https://github.com/mkouhei/bootstrap-py',
      classifiers=classifiers,
      packages=['bootstrap_py'],
      data_files=[],
      install_requires=requires,
      include_package_data=True,
      extras_require=extras_require,
      tests_require=['tox'],
      cmdclass={'test': Tox},
      entry_points={
          'console_scripts': ['bootstrap-py = bootstrap_py.commands:main']
      },)
