# -*- coding: utf-8 -*-
"""bootstrap_py.commands."""
import os
import sys
import re
import argparse
from bootstrap_py import control, __prog__, __version__
from bootstrap_py.update import Update
from bootstrap_py.exceptions import BackendFailure, Conflict


def setoption(parser, metadata=None):
    """Set argument parser option."""
    parser.add_argument('-v', action='version',
                        version=__version__)
    subparsers = parser.add_subparsers(help='sub commands help')
    create_cmd = subparsers.add_parser('create')
    create_cmd.add_argument('name',
                            help='Specify Python package name.')
    create_cmd.add_argument('-d', dest='description', action='store',
                            help='Short description about your package.')
    create_cmd.add_argument('-a', dest='author', action='store',
                            required=True,
                            help='Python package author name.')
    create_cmd.add_argument('-e', dest='email', action='store',
                            required=True,
                            help='Python package author email address.')
    create_cmd.add_argument('-l', dest='license',
                            choices=metadata.licenses().keys(),
                            default='GPLv3+',
                            help='Specify license. (default: %(default)s)')
    create_cmd.add_argument('-s', dest='status',
                            choices=metadata.status().keys(),
                            default='Alpha',
                            help=('Specify development status. '
                                  '(default: %(default)s)'))
    create_cmd.add_argument('--no-check', action='store_true',
                            help='No checking package name in PyPI.')
    create_cmd.add_argument('--with-samples', action='store_true',
                            help='Generate package with sample code.')
    group = create_cmd.add_mutually_exclusive_group(required=True)
    group.add_argument('-U', dest='username', action='store',
                       help='Specify GitHub username.')
    group.add_argument('-u', dest='url', action='store', type=valid_url,
                       help='Python package homepage url.')
    create_cmd.add_argument('-o', dest='outdir', action='store',
                            default=os.path.abspath(os.path.curdir),
                            help='Specify output directory. (default: $PWD)')
    list_cmd = subparsers.add_parser('list')
    list_cmd.add_argument('-l', dest='licenses', action='store_true',
                          help='show license choices.')


def valid_url(url):
    """Validate url.

    :rtype: str
    :return: url

    :param str url: package homepage url.
    """
    regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not regex.match(url):
        raise argparse.ArgumentTypeError('"{0}" is invalid url.'.format(url))
    return url


def parse_options(metadata):
    """Parse argument options."""
    parser = argparse.ArgumentParser(description='%(prog)s usage:',
                                     prog=__prog__)
    setoption(parser, metadata=metadata)
    return parser


def main():
    """Execute main processes."""
    try:
        pkg_version = Update()
        if pkg_version.updatable():
            pkg_version.show_message()
        metadata = control.retreive_metadata()
        parser = parse_options(metadata)
        argvs = sys.argv
        if len(argvs) <= 1:
            parser.print_help()
            sys.exit(1)
        args = parser.parse_args()
        control.print_licences(args, metadata)
        control.check_repository_existence(args)
        control.check_package_existence(args)
        control.generate_package(args)
    except (RuntimeError, BackendFailure, Conflict) as exc:
        sys.stderr.write('{0}\n'.format(exc))
        sys.exit(1)


if __name__ == '__main__':
    main()
