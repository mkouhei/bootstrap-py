# -*- coding: utf-8 -*-
"""bootstrap_py.vcs."""
import git


class VCS(object):
    """VCS class."""

    def __init__(self, repo_dir, metadata):
        """Initialize."""
        self.metadata = metadata
        # repo_dir is outdir
        self.repo = git.Git(repo_dir)
        self.init()
        self.config()
        self.add_index()
        self.initial_commit()
        if hasattr(self.metadata, 'username') and self.metadata.username:
            self.remote_add()

    def init(self):
        """git init."""
        self.repo.init()

    def add_index(self):
        """git add ."""
        self.repo.add('.')

    def config(self):
        """git config."""
        self.repo.config('user.name', self.metadata.author)
        self.repo.config('user.email', self.metadata.email)

    def initial_commit(self):
        """initial commit."""
        self.repo.commit('-m', 'Initial commit.')

    def remote_add(self):
        """git remote add."""
        self.repo.remote('add',
                         'origin',
                         'git@github.com:{username}/{repo}.git'.format(
                             username=self.metadata.username,
                             repo=self.metadata.name))
