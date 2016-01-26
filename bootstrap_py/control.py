# -*- coding: utf-8 -*-
"""bootstrap_py.control."""
import os
import shutil
import tempfile
from jinja2 import PackageLoader, Environment


# pylint: disable=too-few-public-methods
class PackageData(object):
    """Package meta data class."""

    def _set_param(self, name, value):
        """set name:value property to Package object."""
        setattr(self, name, value)

    def __init__(self, args):
        """Initialize Package."""
        if hasattr(args, '_get_kwargs'):
            for name, value in vars(args).items():
                self._set_param(name, value)


class PackageTree(object):
    """Package directory tree class."""

    template_name = 'bootstrap_py'
    init = '__init__.py'
    dir_perm = 0o755
    pkg_dirs = ['{name}', '{name}/tests', 'utils']

    def __init__(self, package_name, outdir):
        """Initialize."""
        self.name = package_name
        self.outdir = os.path.abspath(outdir)
        self.tmpdir = tempfile.mkdtemp(suffix='bootstrap-py')
        self.templates = None

    def _modname(self, dir_path):
        return dir_path.format(name=self.name).replace('/', '.')

    def _init_py(self, dir_path):
        return os.path.join(dir_path.format(name=self.name), self.init)

    def _generate_dirs(self):
        for dir_path in self.pkg_dirs:
            if not os.path.isdir(dir_path.format(name=self.name)):
                os.makedirs(dir_path.format(name=self.name), self.dir_perm)

    def _list_module_dirs(self):
        return [dir_path for dir_path in self.pkg_dirs
                if dir_path.find('{name}') == 0]

    def _generate_init(self):
        env = Environment(loader=PackageLoader(self.template_name))

        tmpl = env.get_template('__init__.py.j2')

        for dir_path in self._list_module_dirs():
            if not os.path.isfile(self._init_py(dir_path)):
                with open(self._init_py(dir_path), 'w') as fobj:
                    fobj.write(
                        # pylint: disable=no-member
                        tmpl.render(module_name=self._modname(dir_path)))

    def copy(self):
        """Copy directory from working directory to output directory."""
        shutil.copytree(self.tmpdir, os.path.join(self.outdir, self.name))

    def clean(self):
        """Clean up working directory."""
        shutil.rmtree(self.tmpdir)

    def generate(self):
        """Generate package directory tree."""
        self._generate_dirs()
        self._generate_init()
