# -*- coding: utf-8 -*-
"""bootstrap_py.commands."""
import os
import sys
import argparse
from bootstrap_py import control, pypi, __version__
from bootstrap_py.classifiers import Classifiers
from bootstrap_py.exceptions import BackendFailure


def setoption(parser, metadata=None):
    """Set argument parser option."""
    parser.add_argument('-v', action='version',
                        version=__version__)
    parser.add_argument('name',
                        help='Specify Python package name.')
    parser.add_argument('-d', dest='description', action='store',
                        help='Short description about your package.')
    parser.add_argument('-a', dest='author', action='store',
                        required=True,
                        help='Python package author name.')
    parser.add_argument('-e', dest='email', action='store',
                        required=True,
                        help='Python package author email address.')
    parser.add_argument('-l', dest='license',
                        choices=metadata.licenses().keys(),
                        default='GPLv3+',
                        help='Specify license.')
    parser.add_argument('-s', dest='status',
                        choices=metadata.status().keys(),
                        default='Alpha',
                        help='Specify development status.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-U', dest='username', action='store',
                       help='Specify GitHub username.')
    group.add_argument('-u', dest='url', action='store',
                       help='Python package homepage url.')


def set_default_options(parser):
    """default options."""
    parser.add_argument('-o', dest='outdir', action='store',
                        default=os.path.abspath(os.path.curdir),
                        help='Specify output directory.')


def parse_options(metadata):
    """setup options."""
    parser = argparse.ArgumentParser(description='usage')
    setoption(parser, metadata=metadata)
    set_default_options(parser)
    return parser.parse_args()


def main():
    """main function."""
    try:
        metadata = Classifiers()
        args = parse_options(metadata)
        if pypi.package_existent(args.name):
            msg = ('[error] "{0}" is registered already in PyPI.\n'
                   '\tSpecify another package name.\n').format(args.name)
            sys.stderr.write(msg)
            sys.exit(1)
        pkg_data = control.PackageData(args)
        pkg_tree = control.PackageTree(pkg_data)
        pkg_tree.generate()
        pkg_tree.move()
    except (RuntimeError, BackendFailure) as exc:
        sys.stderr.write('{0}\n'.format(exc))
        sys.exit(1)


if __name__ == '__main__':
    main()
