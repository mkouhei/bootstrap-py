# -*- coding: utf-8 -*-
"""bootstrap_py.docs."""
import shlex
import subprocess


def build_sphinx(pkg_data, projectdir):
    """Building sphinx documentation.

    :rtype: int
    :return: subprocess.call return code

    :param `bootstrap_py.control.PackageData` pkg_data: package meta data
    :param str projectdir: project root directory
    """
    if len(pkg_data.version.rsplit('.', 1)) > 0:
        version = pkg_data.version.rsplit('.', 1)[0]
    else:
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
    return subprocess.call(shlex.split(args))
