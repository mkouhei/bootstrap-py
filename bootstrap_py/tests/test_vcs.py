# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_vcs."""
import unittest
import shutil
import tempfile
from bootstrap_py.vcs import VCS
from bootstrap_py.tests.test_package import Dummy


class VCSTests(unittest.TestCase):
    """bootstrap_py.vcs.VCS tests."""

    def setUp(self):
        """Prepare test data."""
        self.testdir = tempfile.mkdtemp(suffix='-bootstrap-py-vcs-test')
        self.metadata = Dummy()
        setattr(self.metadata, 'name', 'foobar')
        setattr(self.metadata, 'author', 'Alice Forest')
        setattr(self.metadata, 'email', 'alice@example.org')
        setattr(self.metadata, 'username', 'alice')

    def tearDown(self):
        """cleanup."""
        shutil.rmtree(self.testdir)

    def test_vcs_initialize(self):
        """initialize vcs reporitory."""
        repo = VCS(self.testdir, self.metadata)
        cfg_r = repo.repo.config_reader()
        # pylint: disable=no-member
        self.assertEqual(cfg_r.get('user', 'name'), 'Alice Forest')
        self.assertEqual(cfg_r.get('user', 'email'), 'alice@example.org')
        self.assertEqual(cfg_r.get('remote "origin"', 'url'),
                         'git@github.com:alice/foobar.git')
        self.assertEqual(cfg_r.get('remote "origin"', 'fetch'),
                         '+refs/heads/*:refs/remotes/origin/*')
        cfg_r.release()
        # pylint: disable=no-member
        self.assertTrue(
            'Initial commit.' in repo.repo.refs[0].log()[0].message)
