# -*- coding: utf-8 -*-
"""bootstrap_py.commands."""
import sys
import argparse
from bootstrap_py import __version__


def setoption(parser, keyword):
    """Set argument parser option."""
    if keyword == 'version':
        parser.add_argument('-v', '--version', action='version',
                            version=__version__)
    elif keyword == 'name':
        parser.add_argument('name', nargs=1,
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
    elif keyword == 'url':
        parser.add_argument('-u', '--url', action='store',
                            help='Python package homepage url.')
    elif keyword == 'license':
        parser.add_argument('-l', '--license', action='store',
                            help='Specify license.')


def parse_options():
    """setup options."""
    parser = argparse.ArgumentParser(description='usage')
    setoption(parser, 'version')
    setoption(parser, 'name')
    setoption(parser, 'description')
    setoption(parser, 'author')
    setoption(parser, 'author_email')
    setoption(parser, 'url')
    setoption(parser, 'license')
    return parser.parse_args()


def main():
    """main function."""
    try:
        args = parse_options()
        args.func(args)
    except RuntimeError as exc:
        sys.stderr.write(exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
