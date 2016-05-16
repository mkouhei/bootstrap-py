ChangeLog
=========

0.5.1 (2016-05-17)
------------------

* Adds ``--doctest-modules`` option.
* Fixes pylint option argument.
* Removes doctest exception sample.

Changes follows when enable doctest-modules.::
    
  diff --git a/pytest.ini b/pytest.ini
  index 635a7f9..15cc929 100644
  --- a/pytest.ini
  +++ b/pytest.ini
  @@ -7,6 +7,7 @@ addopts =
           --cov your_package_name
           --cov-report=term
           --cov-report=html
  +        --doctest-modules
   pep8ignore =
           setup.py ALL
           docs/source/conf.py ALL
  diff --git a/tox.ini b/tox.ini
  index 141d468..b8c1f32 100644
  --- a/tox.ini
  +++ b/tox.ini
  @@ -10,7 +10,7 @@ envlist =
   
   [testenv]
   commands =
  -    py.test --pylint --pylint-rcfile={toxinidir}/.pylintrc
  +    py.test --pylint --pylint-rcfile={toxinidir}/.pylintrc your_package_name
   
   [py]
   deps=

0.5.0 (2016-05-07)
------------------

* Adds ``--with-samples`` options; generating sample code.
* Fixes bugs module name when package name includes hyphen.
* Fixes comparing verson bug in updatable for Python3.
* Some refactorings.

0.4.8 (2016-04-25)
------------------

* Fixes warning of build sphinx without docs/source/_static directory.
* Unsupports IP address url.

0.4.7 (2016-04-24)
------------------

* Adds url validator.
* Adds long description checker.

0.4.6 (2016-04-21)
------------------

* Fixes .travis.yml template.

Generated package with v0.4.5 or less that has bugs .travis.yml configuration file.
Modify the follows manually.::

  diff --git a/.travis.yml b/.travis.yml
  index ab128da..600125e 100644
  --- a/.travis.yml
  +++ b/.travis.yml
  @@ -14,6 +14,11 @@ after_success:
     - coveralls --verbose
  
   matrix:
  +  allow_failures:
  +    - env: TOX_ENV=py27
  +    - env: TOX_ENV=py33
  +    - env: TOX_ENV=py34
  +    - env: TOX_ENV=pypy
     include:
  -    python: 3.5
  -    env: TOX_ENV=py35
  +    - python: 3.5
  +      env: TOX_ENV=py35

0.4.5 (2016-04-06)
------------------

* Fixes tox.ini template.

Generated package with v0.4.4 or less that has bugs tox.ini configuration file.
Modify the follows manually.

* Fixes `your_package_name` with snake case. Modify the follows manually.::

    diff --git a/tox.ini b/tox.ini
    index a9d823f..db825cc 100644
    --- a/tox.ini
    +++ b/tox.ini
    @@ -49,7 +49,7 @@ basepython = pypy
    [testenv:pep257]
    deps=
        pep257
    -commands = pep257 bootstrap_py
    +commands = pep257 your_package_name
    basepython = python3.5
    
    [testenv:docs]

0.4.4 (2016-04-05)
------------------

* Adds symlink to pre-commit hook.

Generated package with v0.4.3 or less that has bugs pre-commit hook script.
Modify the follows manually.::

  $ chmod +x utils/pre-commit
  $ ln -s ../../utils/pre-commit .git/hooks/pre-commit

0.4.3 (2016-04-04)
------------------

* Fixes pre-commit hook script permission.

0.4.2 (2016-03-08)
------------------

* Fixes configiratuon version, release.
* Fixes url, author_email in setup.py.
    
Genarated package with v0.4.1 or less that has bugs Sphinx documentation.
Modify the follows manually.

* Fixes ``docs/source/index.rst``::

    diff --git a/docs/source/index.rst b/docs/source/index.rst
    index b3404ac..d8bdc83 100644
    --- a/docs/source/index.rst
    +++ b/docs/source/index.rst
    @@ -16,8 +16,8 @@ Contents:
    
        CHANGELOG
    
    - Indices and tables
    -===================
    +Indices and tables
    +==================
    
     * :ref:`genindex`
     * :ref:`modindex`

* Renames ``docs/source/README`` to ``docs/source/README.rst``.
* Fixes documentation ``version`` in ``docs/source/conf.py``.
* Fixes ``auth_email``, ``url`` in ``setup.py``.

0.4.1 (2016-03-07)
------------------

* Adds exception handler package update.
* Fixes some docstring.

0.4.0 (2016-03-07)
------------------

* Adds checking latest version.
* Fixes Sphinx template bugs.
* Does some refactoring.

0.3.0 (2016-02-21)
------------------

* git init and initial commit.
* Adds --no-check option.
* Fixes list subcommand.

0.2.1 (2016-02-16)
------------------

* Fixes failing create sub-command.

0.2.0 (2016-02-15)
------------------

* Adds create, list sub-command.

  * "create":  generating Python package.
  * "list":    Print license description for choices.

* Changes mutually exclusive group; username, url options.
* Add checking package name in PyPI.
* Adds some exception handling.

0.1.1 (2016-02-02)
------------------

* Fixes README template


0.1.0 (2016-02-02)
------------------

* First release
