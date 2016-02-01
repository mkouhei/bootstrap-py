# -*- coding: utf-8 -*-
"""bootstrap_py.commands."""
import os
import sys
import argparse
from bootstrap_py import control, __version__
from bootstrap_py.classifiers import Classifiers

# ToDo:
# * Genarete Sphinx documentation


def setoption(parser, keyword, metadata=None):
    """Set argument parser option."""
    if keyword == 'version':
        parser.add_argument('-v', '--version', action='version',
                            version=__version__)
    elif keyword == 'name':
        parser.add_argument('name',
                            help='Specify Python package name.')
    elif keyword == 'description':
        parser.add_argument('-d', '--description', action='store',
                            help='Short description about your package.')
    elif keyword == 'author':
        parser.add_argument('-a', '--author', action='store',
                            required=True,
                            help='Python package author name.')
    elif keyword == 'author_email':
        parser.add_argument('-e', '--email', action='store',
                            required=True,
                            help='Python package author email address.')
    elif keyword == 'username':
        parser.add_argument('-U', '--username', action='store',
                            help='Specify GitHub username')
    elif keyword == 'url':
        parser.add_argument('-u', '--url', action='store',
                            help='Python package homepage url.')
    elif keyword == 'license':
        parser.add_argument('-l', '--license',
                            choices=metadata.licenses().keys(),
                            default='GPLv3+',
                            help='Specify license.')
    elif keyword == 'status':
        parser.add_argument('-s', '--status',
                            choices=metadata.status().keys(),
                            default='Alpha',
                            help='Specify development status.')


def set_default_options(parser):
    """default options."""
    parser.add_argument('-o', '--outdir', action='store',
                        default=os.path.abspath(os.path.curdir),
                        help='Specify output directory.')


def parse_options(metadata):
    """setup options."""
    parser = argparse.ArgumentParser(description='usage')
    setoption(parser, 'version')
    setoption(parser, 'name')
    setoption(parser, 'description')
    setoption(parser, 'author')
    setoption(parser, 'author_email')
    setoption(parser, 'username')
    setoption(parser, 'url')
    setoption(parser, 'license', metadata=metadata)
    setoption(parser, 'status', metadata=metadata)
    set_default_options(parser)
    return parser.parse_args()


def main():
    """main function."""
    try:
        metadata = Classifiers()
        args = parse_options(metadata)
        pkg_data = control.PackageData(args)
        pkg_tree = control.PackageTree(pkg_data)
        pkg_tree.generate()
        pkg_tree.move()
    except RuntimeError as exc:
        sys.stderr.write(exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
