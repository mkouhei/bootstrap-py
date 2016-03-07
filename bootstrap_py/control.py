# -*- coding: utf-8 -*-
"""bootstrap_py.control."""
import os
import sys
from bootstrap_py import package, pypi
from bootstrap_py.classifiers import Classifiers
from bootstrap_py.vcs import VCS
from bootstrap_py.exceptions import Conflict


def _pp(dict_data):
    """pretty print."""
    for key, val in dict_data.items():
        # pylint: disable=superfluous-parens
        print('{0:<11}: {1}'.format(key, val))


def retreive_metadata():
    """retrieve metadata.

    :rtype: bootstrap_py.classifiers.Classifiers
    :return: Classifiers()
    """
    return Classifiers()


def print_licences(params, metadata):
    """print licenses.

    :param argparse.Namespace params: parameter
    :param bootstrap_py.classifier.Classifiers metadata: package metadata
    """
    if hasattr(params, 'licenses'):
        if params.licenses:
            _pp(metadata.licenses_desc())
        sys.exit(0)


def check_repository_existence(params):
    """check repository existence.

    :param argparse.Namespace params: parameters
    """
    repodir = os.path.join(params.outdir, params.name)
    if os.path.isdir(repodir):
        raise Conflict(
            'Package repository "{0}" has already exists.'.format(repodir))


def check_package_existence(params):
    """check package existence.

    :param argparse.Namespace params: parameters
    """
    if not params.no_check:
        pypi.package_existent(params.name)


def generate_package(params):
    """generate package repository.

    :param argparse.Namespace params: parameters
    """
    pkg_data = package.PackageData(params)
    pkg_tree = package.PackageTree(pkg_data)
    pkg_tree.generate()
    pkg_tree.move()
    VCS(os.path.join(pkg_tree.outdir, pkg_tree.name), pkg_tree.pkg_data)
