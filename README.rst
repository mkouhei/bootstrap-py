==========================
 Bootstrap Python Package
==========================

The ``bootstrap-py`` provides generating the Python packages.

Status
======

.. image:: https://github.com/mkouhei/bootstrap-py/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/mkouhei/bootstrap-py/actions/workflows/ci.yml?query=branch%3Amaster
.. image:: https://coveralls.io/repos/mkouhei/bootstrap-py/badge.png?branch=master
   :target: https://coveralls.io/r/mkouhei/bootstrap-py?branch=master
.. image:: https://img.shields.io/pypi/v/bootstrap-py.svg
   :target: https://pypi.python.org/pypi/bootstrap-py
.. image:: https://readthedocs.org/projects/bootstrap-py/badge/?version=latest
   :target: https://readthedocs.org/projects/bootstrap-py/?badge=latest
   :alt: Documentation Status

Requirements
============

* Python 3.9 over

Features
========

* Generating Python package.
* Checking Python package name existence at PyPI.
* Test and conde checking environment is configured with the `Tox <https://pypi.python.org/pypi/tox>`_, `Pytest <http://pytest.org/latest-ja/>`_, and others.

  * `pycodestyle <https://pypi.python.org/pypi/pycodestyle>`_
  * `pytest-cov <https://pypi.python.org/pypi/pytest-cov>`_
  * `pytest-flake8 <https://pypi.python.org/pypi/pytest-flake8>`_
  * `pydocstyle <https://pypi.org/project/pydocstyle/>`_

* Generating documentation automatically with the `Sphinx <http://www.sphinx-doc.org/en/stable/>`_.
* Configuration Git repository, initial commit.
* Generate sample code using ``--with-samples`` option.

Usage
=====

Install bootstrap-py
--------------------

Install bootstrap-py::

  $ python -m venv .venv
  $ python -m pip install bootstrap-py

Generate Python package
-----------------------

Generate your Python package.::

  $ .venv/bin/bootstrap-py create -a 'Your author name' -e 'your-author-email@example.org' \
  -u 'https://your-package-website.example.org' -o '/path/to/package-dir' \
  -l 'select-the-license' 'your-package-name'
  $ ls -a package-dir
  .  ..  .coveragerc  .git  .github  .gitignore  MANIFEST.in  README.rst  docs  pyproject.toml  src  tox.ini  utils


List license choices
--------------------

List license description choices.::

  $ .venv/bin/bootstrap-py list -l
  GPL        : GNU General Public License (GPL)
  CPL        : Common Public License
  IOSL       : Intel Open Source License
  GPLv3+     : GNU General Public License v3 or later (GPLv3+)
  (omit)


Using tox
---------

Running test with tox::

  $ pip install --user tox
  $ tox
  (omit)
  _______________________________________ summary ______________________________________
  py311: commands succeeded
  flake8: commands succeeded
  pycodetyle: commands succeeded
  pydocstyle: commands succeeded
  docs: commands succeeded
  congratulations :)

