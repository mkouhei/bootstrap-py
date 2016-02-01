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
import requests_mock
from bootstrap_py import commands, __version__
from bootstrap_py.classifiers import Classifiers


class CommandsTests(unittest.TestCase):
    """bootstrap_py.commands tests."""

    def setUp(self):
        """Prepare tests."""
        with requests_mock.Mocker() as mock:
            with open('bootstrap_py/data/classifiers.txt') as fobj:
                data = fobj.read()
            mock.get(Classifiers.url,
                     text=data,
                     status_code=200)
            self.metadata = Classifiers()
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
        commands.setoption(self.parser, 'version')
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
            commands.parse_options(self.metadata)
        self.assertEqual(2, exc.exception.code)
        self.assertTrue(sys.stderr.getvalue())

    def test_setoption_name(self):
        """parse argument name."""
        commands.setoption(self.parser, 'name')
        self.assertEqual('foo',
                         self.parser.parse_args('foo'.split()).name)

    def test_setoption_author(self):
        """parse argument author."""
        commands.setoption(self.parser, 'author')
        self.assertEqual(
            'Alice Forest',
            self.parser.parse_args(shlex.split('-a "Alice Forest"')).author)

    def test_setoption_author_email(self):
        """parse argument email."""
        commands.setoption(self.parser, 'author_email')
        self.assertEqual(
            'alice@example.org',
            self.parser.parse_args(shlex.split('-e alice@example.org')).email)

    def test_setoption_description(self):
        """parse argument description."""
        commands.setoption(self.parser, 'description')
        self.assertEqual(
            'short description.',
            self.parser.parse_args(
                shlex.split('-d "short description."')).description)

    def test_setoption_url(self):
        """parse argument url."""
        commands.setoption(self.parser, 'url')
        self.assertEqual(
            'http://example.org',
            self.parser.parse_args(shlex.split('-u http://example.org')).url)

    def test_setoption_username(self):
        """parse argument username."""
        commands.setoption(self.parser, 'username')
        self.assertEqual(
            'alice',
            self.parser.parse_args(shlex.split('-U alice')).username)

    def test_setoption_status(self):
        """parse argument status."""
        commands.setoption(self.parser, 'status', metadata=self.metadata)
        self.assertEqual(
            'Alpha',
            self.parser.parse_args(shlex.split('-s Alpha')).status)

    def test_setoption_license(self):
        """parse argument license."""
        commands.setoption(self.parser, 'license', metadata=self.metadata)
        self.assertEqual(
            'GPLv3+',
            self.parser.parse_args(shlex.split('-l GPLv3+')).license)

    def test_setoption_default_options(self):
        """parse argument default options."""
        commands.set_default_options(self.parser)
        self.assertEqual(
            '/path/to/outdir',
            self.parser.parse_args(shlex.split('-o /path/to/outdir')).outdir)

    def test_main_fail_to_parse(self):
        """main fail."""
        with requests_mock.Mocker() as mock:
            with open('bootstrap_py/data/classifiers.txt') as fobj:
                data = fobj.read()
            mock.get(Classifiers.url,
                     text=data,
                     status_code=200)
            with self.assertRaises(SystemExit) as exc:
                commands.main()
        self.assertEqual(2, exc.exception.code)
        self.assertTrue(sys.stderr.getvalue())
