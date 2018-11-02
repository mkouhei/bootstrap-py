# -*- coding: utf-8 -*-
"""bootstrap_py.vcs."""
import os
import git


# pylint: disable=too-few-public-methods
class VCS:
    """VCS class."""

    def __init__(self, repo_dir, metadata):
        """Initialize."""
        self.metadata = metadata
        self.repo = git.Repo.init(os.path.join(repo_dir))
        self._config()
        self._add_index()
        self._initial_commit()
        if hasattr(self.metadata, 'username') and self.metadata.username:
            self._remote_add()
        # work around: git.Repo.init write ref to .git/HEAD without line feed.
        with open(os.path.join(repo_dir, '.git/HEAD')) as fobj:
            data = fobj.read()
        if data.rfind('\n') == -1:
            with open(os.path.join(repo_dir, '.git/HEAD'), 'a') as fobj:
                fobj.write('\n')

        # adds pre-commit hook
        os.symlink('../../utils/pre-commit',
                   os.path.join(repo_dir, '.git/hooks/pre-commit'))

    def _add_index(self):
        """Execute git add ."""
        self.repo.index.add(self.repo.untracked_files)

    def _config(self):
        """Execute git config."""
        cfg_wr = self.repo.config_writer()
        cfg_wr.add_section('user')
        cfg_wr.set_value('user', 'name', self.metadata.author)
        cfg_wr.set_value('user', 'email', self.metadata.email)
        cfg_wr.release()

    def _initial_commit(self):
        """Initialize commit."""
        self.repo.index.commit('Initial commit.')

    def _remote_add(self):
        """Execute git remote add."""
        self.repo.create_remote(
            'origin',
            'git@github.com:{username}/{repo}.git'.format(
                username=self.metadata.username,
                repo=self.metadata.name))
