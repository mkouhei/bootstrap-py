# -*- coding: utf-8 -*-
"""bootstrap_py.tests.test_package."""
import unittest
import os
import shutil
import tempfile
from glob import glob
from datetime import datetime
from mock import patch
from bootstrap_py import package
from bootstrap_py.tests.stub import stub_request_metadata


# pylint: disable=too-few-public-methods
class Dummy:
    """Dummy class."""


class PackageDataTests(unittest.TestCase):
    """bootstrap_py.package.PackageData tests."""

    def setUp(self):
        """Prepare test data."""
        self.params = Dummy()
        setattr(self.params, 'foo', 'hoge')
        setattr(self.params, 'bar', 'moge')
        setattr(self.params, 'baz', 'fuga')

        self.default_params = Dummy()
        setattr(self.default_params, 'date', '2016-01-29')
        setattr(self.default_params, 'version', '1.0.0')
        setattr(self.default_params, 'description', 'dummy description.')
        self.metadata = stub_request_metadata()

    def test_provides_params(self):
        """provides params without default params."""
        pkg_data = package.PackageData(self.params)
        # pylint: disable=no-member
        self.assertEqual(pkg_data.foo, 'hoge')
        self.assertEqual(pkg_data.bar, 'moge')
        self.assertEqual(pkg_data.baz, 'fuga')
        self.assertEqual(pkg_data.date, datetime.utcnow().strftime('%Y-%m-%d'))
        self.assertEqual(pkg_data.version, '0.1.0')
        # pylint: disable=fixme
        self.assertEqual(pkg_data.description, '##### ToDo: Rewrite me #####')

    def test_provides_default_params(self):
        """provides params without default params."""
        pkg_data = package.PackageData(self.default_params)
        # pylint: disable=no-member
        self.assertEqual(pkg_data.date, '2016-01-29')
        self.assertEqual(pkg_data.version, '1.0.0')
        self.assertEqual(pkg_data.description, 'dummy description.')

    def test_convert_to_dict(self):
        """convert PackageData to dict."""
        dict_data = package.PackageData(self.default_params).to_dict()
        # pylint: disable=no-member
        self.assertEqual(dict_data.get('date'), '2016-01-29')
        self.assertEqual(dict_data.get('version'), '1.0.0')
        self.assertEqual(dict_data.get('description'), 'dummy description.')


class PackageTreeTests(unittest.TestCase):
    """bootstrap.package.PackageTree tests."""

    def setUp(self):
        """Prepare test data."""
        self.cwd = os.getcwd()
        self.testdir = tempfile.mkdtemp(suffix='-bootstrap-py-test')
        params = Dummy()
        setattr(params, 'name', 'foo')
        setattr(params, 'author', 'Alice')
        setattr(params, 'email', 'alice@example.org')
        setattr(params, 'url', 'https://example.org/foo')
        setattr(params, 'license', 'gplv3')
        setattr(params, 'outdir', self.testdir)
        setattr(params, 'with_samples', True)
        stub_request_metadata()
        self.pkg_data = package.PackageData(params)
        self.pkg_tree = package.PackageTree(self.pkg_data)

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.testdir)
        if os.path.isdir(self.pkg_tree.tmpdir):
            self.pkg_tree.clean()

    def test_initialize(self):
        """initialize PackageTree."""
        self.assertEqual(self.pkg_tree.name, 'foo')
        self.assertEqual(self.pkg_tree.outdir, self.testdir)
        self.assertTrue(os.path.isdir(self.pkg_tree.tmpdir))
        self.assertEqual(len(self.pkg_tree.templates.list_templates()), 18)
        self.assertEqual(self.pkg_tree.pkg_data, self.pkg_data)

    def test_init_py(self):
        """convert __init__.py path."""
        self.assertEqual(getattr(self.pkg_tree, '_init_py')('foo/bar'),
                         os.path.join(self.pkg_tree.tmpdir,
                                      'foo/bar/__init__.py'))

    def test_tmpl_path(self):
        """convert tmplate path."""
        self.assertEqual(getattr(self.pkg_tree, '_tmpl_path')('foo.py.j2'),
                         os.path.join(self.pkg_tree.tmpdir,
                                      'foo.py'))

    def test_generate_dirs(self):
        """generate directories."""
        getattr(self.pkg_tree, '_generate_dirs')()
        os.chdir(self.pkg_tree.tmpdir)
        self.assertTrue(os.path.isdir(self.pkg_tree.pkg_data.module_name))
        self.assertTrue(os.path.isdir(
            os.path.join(self.pkg_tree.pkg_data.module_name,
                         'tests')))
        self.assertTrue(os.path.isdir('utils'))
        self.assertTrue(os.path.isdir('docs/source/modules'))

    def test_list_module_dirs(self):
        """list module directories."""
        self.assertEqual(getattr(self.pkg_tree, '_list_module_dirs')(),
                         ['{module_name}', '{module_name}/tests'])

    def test_generate_init(self):
        """generate __init__.py."""
        getattr(self.pkg_tree, '_generate_dirs')()
        getattr(self.pkg_tree, '_generate_init')()
        os.chdir(self.pkg_tree.tmpdir)
        self.assertTrue(os.path.isfile('foo/__init__.py'))
        self.assertTrue(os.path.isfile('foo/tests/__init__.py'))

    def test_generate_files(self):
        """generate files."""
        getattr(self.pkg_tree, '_generate_dirs')()
        getattr(self.pkg_tree, '_generate_files')()
        os.chdir(self.pkg_tree.tmpdir)
        self.assertEqual(len([i for i in glob('./*')
                              if os.path.isfile(i)]), 6)
        self.assertEqual(len([i for i in glob('./.*')
                              if os.path.isfile(i)]), 5)
        self.assertEqual(len([i for i in glob('utils/*')
                              if os.path.isfile(i)]), 1)
        self.assertEqual(len([i for i in glob('docs/source/*')
                              if os.path.isfile(i)]), 3)
        self.assertEqual(len([i for i in glob('docs/source/modules/*')
                              if os.path.isfile(i)]), 1)

    def test_generate_files_samples(self):
        """generate files."""
        self.pkg_data.with_samples = True
        getattr(self.pkg_tree, '_generate_dirs')()
        getattr(self.pkg_tree, '_generate_files')()
        os.chdir(self.pkg_tree.tmpdir)
        self.assertEqual(len([i for i in glob('./*')
                              if os.path.isfile(i)]), 6)
        self.assertEqual(len([i for i in glob('./.*')
                              if os.path.isfile(i)]), 5)
        self.assertEqual(len([i for i in glob('foo/*')
                              if os.path.isfile(i)]), 2)
        self.assertEqual(len([i for i in glob('foo/tests/*')
                              if os.path.isfile(i)]), 2)
        self.assertEqual(len([i for i in glob('utils/*')
                              if os.path.isfile(i)]), 1)
        self.assertEqual(len([i for i in glob('docs/source/*')
                              if os.path.isfile(i)]), 3)
        self.assertEqual(len([i for i in glob('docs/source/modules/*')
                              if os.path.isfile(i)]), 1)

    def test_move(self):
        """move source directory to destination directory."""
        self.pkg_tree.move()
        self.assertFalse(os.path.isdir(self.pkg_tree.tmpdir))
        self.assertTrue(os.path.isdir(self.testdir))

    @patch('subprocess.call')
    def test_generate(self, _mock):
        """generate directories, and files."""
        popen_mock = _mock.return_value
        popen_mock.wait = None
        popen_mock.call = None
        self.pkg_tree.generate()
        os.chdir(self.pkg_tree.tmpdir)
        self.assertTrue(os.path.isdir(self.pkg_tree.name))
        self.assertTrue(os.path.isdir(os.path.join(self.pkg_tree.name,
                                                   'tests')))
        self.assertTrue(os.path.isdir('utils'))
        self.assertTrue(os.path.isdir('docs/source/modules'))
        self.assertTrue(os.path.isfile('foo/__init__.py'))
        self.assertTrue(os.path.isfile('foo/tests/__init__.py'))
        self.assertEqual(len([i for i in glob('./*')
                              if os.path.isfile(i)]), 6)
        self.assertEqual(len([i for i in glob('./.*')
                              if os.path.isfile(i)]), 5)
        self.assertEqual(len([i for i in glob('utils/*')
                              if os.path.isfile(i)]), 1)
        self.assertEqual(len([i for i in glob('docs/source/*')
                              if os.path.isfile(i)]), 3)
        self.assertEqual(len([i for i in glob('docs/source/modules/*')
                              if os.path.isfile(i)]), 1)

    def test_clean(self):
        """clean up."""
        self.pkg_tree.clean()
        self.assertFalse(os.path.isdir(self.pkg_tree.tmpdir))
