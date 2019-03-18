# -*- coding: utf-8 -*-
"""bootstrap_py.docs."""
import os.path
import shlex
import subprocess


def build_sphinx(pkg_data, projectdir):
    """Build sphinx documentation.

    :rtype: int
    :return: subprocess.call return code

    :param `bootstrap_py.control.PackageData` pkg_data: package meta data
    :param str projectdir: project root directory
    """
    try:
        version, _minor_version = pkg_data.version.rsplit('.', 1)
    except ValueError:
        version = pkg_data.version
    args = ' '.join(('sphinx-quickstart',
                     '--sep',
                     '-q',
                     '-p "{name}"',
                     '-a "{author}"',
                     '-v "{version}"',
                     '-r "{release}"',
                     '-l en',
                     '--suffix=.rst',
                     '--master=index',
                     '--ext-autodoc',
                     '--ext-viewcode',
                     '--makefile',
                     '{projectdir}')).format(name=pkg_data.name,
                                             author=pkg_data.author,
                                             version=version,
                                             release=pkg_data.version,
                                             projectdir=projectdir)
    if subprocess.call(shlex.split(args)) == 0:
        _touch_gitkeep(projectdir)


def _touch_gitkeep(docs_path):
    with open(os.path.join(docs_path,
                           'source',
                           '_static',
                           '.gitkeep'), 'w') as fobj:
        fobj.write('')
