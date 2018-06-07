# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_commands."""
import unittest
import argparse
import os
import shlex
import shutil
import sys
import tempfile
import six
from bootstrap_py import commands, __version__
from bootstrap_py.tests.stub import stub_request_metadata


class CommandsTests(unittest.TestCase):
    """bootstrap_py.commands tests."""

    def setUp(self):
        """Prepare tests."""
        self.metadata = stub_request_metadata()
        self.parser = argparse.ArgumentParser(description='usage')
        self.capture = sys.stdout
        self.capture_error = sys.stderr
        sys.stdout = six.StringIO()
        sys.stderr = six.StringIO()
        self.outdir = tempfile.mkdtemp(suffix='-bootstrap-py-test')

    def tearDown(self):
        """Clean up."""
        sys.stdout = self.capture
        sys.stderr = self.capture_error
        if os.path.isdir(self.outdir):
            shutil.rmtree(self.outdir)

    def test_setoption_version(self):
        """parser add_argument version."""
        commands.setoption(self.parser, self.metadata)
        with self.assertRaises(SystemExit) as exc:
            self.parser.parse_args('-v'.split())
        self.assertEqual(0, exc.exception.code)
        if sys.version_info > (3, 4):
            self.assertEqual(__version__ + '\n', sys.stdout.getvalue())
        else:
            self.assertEqual(__version__ + '\n', sys.stderr.getvalue())

    def test_parse_options_fail(self):
        """fail parse options."""
        with self.assertRaises(SystemExit) as exc:
            parser = commands.parse_options(self.metadata)
            parser.parse_args()
        self.assertEqual(2, exc.exception.code)
        self.assertTrue(sys.stderr.getvalue())

    def test_setoption_minimum_username(self):
        """parse argument minimum with username."""
        commands.setoption(self.parser, self.metadata)
        args = 'create -a "Alice Forest" -e alice@example.org -U alice foo'
        self.assertEqual('foo',
                         self.parser.parse_args(shlex.split(args)).name)
        self.assertEqual('Alice Forest',
                         self.parser.parse_args(shlex.split(args)).author)
        self.assertEqual('alice@example.org',
                         self.parser.parse_args(shlex.split(args)).email)
        self.assertEqual('alice',
                         self.parser.parse_args(shlex.split(args)).username)

    def test_setoption_minimum_url(self):
        """parse argument minimum with url."""
        commands.setoption(self.parser, self.metadata)
        args = ('create -a "Alice Forest" -e alice@example.org '
                '-u http://example.org foo')
        self.assertEqual('foo',
                         self.parser.parse_args(shlex.split(args)).name)
        self.assertEqual('Alice Forest',
                         self.parser.parse_args(shlex.split(args)).author)
        self.assertEqual('alice@example.org',
                         self.parser.parse_args(shlex.split(args)).email)
        self.assertEqual('http://example.org',
                         self.parser.parse_args(shlex.split(args)).url)

    def test_setoption_invalid_url(self):
        """parse argument minimum with url."""
        commands.setoption(self.parser, self.metadata)
        args = ('create -a "Alice Forest" -e alice@example.org '
                '-u http://example foo')
        with self.assertRaises(SystemExit) as exc:
            self.parser.parse_args(shlex.split(args))
        self.assertEqual(2, exc.exception.code)

    def test_setoption_with_extras(self):
        """parse argument extras."""
        commands.setoption(self.parser, self.metadata)
        args = ('create -a "Alice Forest" -e alice@example.org -U alice '
                '-l LGPLv3+ -s Beta foo')
        self.assertEqual('foo',
                         self.parser.parse_args(shlex.split(args)).name)
        self.assertEqual('Alice Forest',
                         self.parser.parse_args(shlex.split(args)).author)
        self.assertEqual('alice@example.org',
                         self.parser.parse_args(shlex.split(args)).email)
        self.assertEqual('alice',
                         self.parser.parse_args(shlex.split(args)).username)
        self.assertEqual('LGPLv3+',
                         self.parser.parse_args(shlex.split(args)).license)
        self.assertEqual('Beta',
                         self.parser.parse_args(shlex.split(args)).status)

    def test_main_fail_to_parse(self):
        """main fail."""
        stub_request_metadata(badge=True)
        with self.assertRaises(SystemExit) as exc:
            commands.main()
        self.assertEqual(2, exc.exception.code)
        self.assertTrue(sys.stderr.getvalue())
