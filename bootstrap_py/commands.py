# -*- coding: utf-8 -*-
"""bootstrap_py.commands."""
import os
import sys
import argparse
from bootstrap_py import control, pypi, __prog__, __version__
from bootstrap_py.classifiers import Classifiers
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
    group = create_cmd.add_mutually_exclusive_group(required=True)
    group.add_argument('-U', dest='username', action='store',
                       help='Specify GitHub username.')
    group.add_argument('-u', dest='url', action='store',
                       help='Python package homepage url.')
    create_cmd.add_argument('-o', dest='outdir', action='store',
                            default=os.path.abspath(os.path.curdir),
                            help='Specify output directory. (default: $PWD)')
    list_cmd = subparsers.add_parser('list')
    list_cmd.add_argument('-l', dest='licenses', action='store_true',
                          help='show license choices.')


def parse_options(metadata):
    """setup options."""
    parser = argparse.ArgumentParser(description='%(prog)s usage:',
                                     prog=__prog__)
    setoption(parser, metadata=metadata)
    return parser.parse_args()


def _pp(dict_data):
    """pretty print."""
    for key, val in dict_data.items():
        # pylint: disable=superfluous-parens
        print('{0:<11}: {1}'.format(key, val))


def main():
    """main function."""
    try:
        metadata = Classifiers()
        args = parse_options(metadata)
        if args.licenses:
            _pp(metadata.licenses_desc())
            sys.exit(0)
        pypi.package_existent(args.name)
        pkg_data = control.PackageData(args)
        pkg_tree = control.PackageTree(pkg_data)
        pkg_tree.generate()
        pkg_tree.move()
    except (RuntimeError, BackendFailure, Conflict) as exc:
        sys.stderr.write('{0}\n'.format(exc))
        sys.exit(1)


if __name__ == '__main__':
    main()
