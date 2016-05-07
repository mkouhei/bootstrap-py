==========================
 Bootstrap Python Package
==========================

The ``bootstrap-py`` provides generating the Python packages.

Status
======

.. image:: https://secure.travis-ci.org/mkouhei/bootstrap-py.png?branch=master
   :target: http://travis-ci.org/mkouhei/bootstrap-py
.. image:: https://coveralls.io/repos/mkouhei/bootstrap-py/badge.png?branch=master
   :target: https://coveralls.io/r/mkouhei/bootstrap-py?branch=master
.. image:: https://img.shields.io/pypi/v/bootstrap-py.svg
   :target: https://pypi.python.org/pypi/bootstrap-py
.. image:: https://readthedocs.org/projects/bootstrap-py/badge/?version=latest
   :target: https://readthedocs.org/projects/bootstrap-py/?badge=latest
   :alt: Documentation Status

Requirements
============

* Python 2.7 over or Python 3.3 over or PyPy 2.4.0 over

Features
========

* Generating Python package.
* Checking Python package name existence at PyPI.
* Test and conde checking environment is configured with the `Tox <https://pypi.python.org/pypi/tox>`_, `Pytest <http://pytest.org/latest-ja/>`_, and others.
    
  * `pytest-cov <https://pypi.python.org/pypi/pytest-cov>`_
  * `pytest-pep8 <https://pypi.python.org/pypi/pytest-pep8>`_
  * `pytest-flakes <https://pypi.python.org/pypi/pytest-flakes>`_
  * `Pylint <http://www.pylint.org/>`_
  * `PyChecker <http://pychecker.sourceforge.net/>`_
  * `pep257 <https://github.com/GreenSteam/pep257/>`_

* Generating documentation automatically with the `Sphinx <http://www.sphinx-doc.org/en/stable/>`_.
* Configuration Git repository, initial commit.
* Generate sample code using ``--with-samples`` option.

Usage
=====

Install bootstrap-py
--------------------

Install bootstrap-py::

  $ virtualenv venv
  $ . venv/bin/activate
  (venv)$ pip install bootstrap-py


Generate Python package
-----------------------

Generate your Python package.::

  (venv)$ bootstrap-py create -a 'Your author name' -e 'your-author-email@example.org' \
  -u 'https://your-package-website.example.org' -o '/path/to/package-dir' \
  -l 'select-the-license' 'your-package-name'
  (venv)$ deactivate
  $ cd /path/to/package-dir
  $ ls
  MANIFEST.in  docs     pytest.ini  setup.py  utils
  README.rst   libneta  setup.cfg   tox.ini


List license choices
--------------------

List license description choices.::

  (venv)$ bootstrap-py list -l
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
  py27: commands succeeded
  py34: commands succeeded
  py35: commands succeeded
  pypy: commands succeeded
  pep257: commands succeeded
  docs: commands succeeded
  pychecker: commands succeeded
  congratulations :)

