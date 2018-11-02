# -*- coding: utf-8 -*-
"""bootstrap_py.package."""
import os
import shutil
import tempfile
from datetime import datetime
from jinja2 import PackageLoader, Environment
from pguard import guard
from pguard import guard_cl as g
from bootstrap_py.classifiers import Classifiers
from bootstrap_py.vcs import VCS
from bootstrap_py.docs import build_sphinx


# pylint: disable=too-few-public-methods
class PackageData:
    """Package meta data class."""

    #: Configured the default "version" of setup.setup().
    default_version = '0.1.0'
    #: Users should rewrite parameters after they generate Python package.
    warning_message = '##### ToDo: Rewrite me #####'  # pylint: disable=fixme

    def __init__(self, args):
        """Initialize Package."""
        self.metadata = Classifiers()
        if hasattr(args, '__dict__'):
            for name, value in vars(args).items():
                self._set_param(name, value)
        self._check_or_set_default_params()

    def _set_param(self, name, value):
        """Set name:value property to Package object."""
        if name == 'status':
            setattr(self, name, self.metadata.status().get(value))
        elif name == 'license':
            setattr(self, name, self.metadata.licenses().get(value))
        elif name == 'name':
            setattr(self, name, value)
            setattr(self, 'module_name', value.replace('-', '_'))
        else:
            setattr(self, name, value)

    def _check_or_set_default_params(self):
        """Check key and set default vaule when it does not exists."""
        if not hasattr(self, 'date'):
            self._set_param('date', datetime.utcnow().strftime('%Y-%m-%d'))
        if not hasattr(self, 'version'):
            self._set_param('version', self.default_version)
        # pylint: disable=no-member
        if not hasattr(self, 'description') or self.description is None:
            getattr(self, '_set_param')('description', self.warning_message)

    def to_dict(self):
        """Convert the package data to dict."""
        return self.__dict__


class PackageTree:
    """Package directory tree class."""

    #: Jinja2 template name
    template_name = 'bootstrap_py'
    #: the suffix name of working directory for generating
    suffix = '-bootstrap-py'
    #: init filename
    init = '__init__.py'
    #: default permission
    exec_perm = 0o755
    #: include directories to packages
    pkg_dirs = ['{module_name}', '{module_name}/tests']

    def __init__(self, pkg_data):
        """Initialize."""
        self.cwd = os.getcwd()
        self.name = pkg_data.name
        self.outdir = os.path.abspath(pkg_data.outdir)
        self.tmpdir = tempfile.mkdtemp(suffix=self.suffix)
        self.templates = Environment(loader=PackageLoader(self.template_name))
        self.pkg_data = pkg_data

    def _init_py(self, dir_path):
        return os.path.join(self.tmpdir,
                            dir_path.format(**self.pkg_data.to_dict()),
                            self.init)

    def _sample_py(self, file_path):
        return os.path.join(self.tmpdir,
                            self.pkg_data.module_name,
                            os.path.splitext(file_path)[0])

    def _tmpl_path(self, file_path):
        return os.path.join(self.tmpdir, os.path.splitext(file_path)[0])

    def _generate_dirs(self):
        dirs = [os.path.dirname(tmpl)
                for tmpl in self.templates.list_templates()
                if tmpl.find('/') > -1] + self.pkg_dirs
        for dir_path in dirs:
            if not os.path.isdir(
                    os.path.join(self.tmpdir,
                                 dir_path.format(**self.pkg_data.to_dict()))):
                os.makedirs(os.path.join(self.tmpdir,
                                         dir_path.format(
                                             **self.pkg_data.to_dict())),
                            self.exec_perm)

    def _generate_docs(self):
        docs_path = os.path.join(self.tmpdir, 'docs')
        os.makedirs(docs_path)
        build_sphinx(self.pkg_data, docs_path)

    def _list_module_dirs(self):
        return [dir_path for dir_path in self.pkg_dirs
                if dir_path.find('{module_name}') == 0]

    def _generate_init(self):
        tmpl = self.templates.get_template('__init__.py.j2')

        for dir_path in self._list_module_dirs():
            if not os.path.isfile(self._init_py(dir_path)):
                with open(self._init_py(dir_path), 'w') as fobj:
                    # pylint: disable=no-member
                    fobj.write(
                        tmpl.render(**self.pkg_data.to_dict()) + '\n')
        return True

    def _generate_file(self, file_path):
        tmpl = self.templates.get_template(file_path)
        with open(self._tmpl_path(file_path), 'w') as fobj:
            fobj.write(
                tmpl.render(**self.pkg_data.to_dict()) + '\n')
        return True

    def _generate_exec_file(self, file_path):
        self._generate_file(file_path)
        os.chmod(self._tmpl_path(file_path), self.exec_perm)
        return True

    def _generate_samples(self, file_path):
        if not self.pkg_data.with_samples:
            return False
        tmpl = self.templates.get_template(file_path)
        if file_path == 'sample.py.j2':
            with open(self._sample_py(file_path), 'w') as fobj:
                fobj.write(
                    tmpl.render(
                        **self.pkg_data.to_dict()) + '\n')
        elif file_path == 'test_sample.py.j2':
            with open(self._sample_py(os.path.join('tests',
                                                   file_path)), 'w') as fobj:
                fobj.write(
                    tmpl.render(
                        **self.pkg_data.to_dict()) + '\n')
        return True

    def _generate_files(self):
        generator = (lambda f: guard(
            g(self._generate_init, f == '__init__.py.j2'),
            g(self._generate_exec_file, f == 'utils/pre-commit.j2', (f,)),
            g(self._generate_samples, f.endswith('sample.py.j2'), (f,)),
            g(self._generate_file, params=(f,))))
        for file_path in self.templates.list_templates():
            generator(file_path)
        os.chdir(self.tmpdir)
        os.symlink('../../README.rst', 'docs/source/README.rst')
        os.chdir(self.cwd)

    def move(self):
        """Move directory from working directory to output directory."""
        if not os.path.isdir(self.outdir):
            os.makedirs(self.outdir)
        shutil.move(self.tmpdir, os.path.join(self.outdir, self.name))

    def clean(self):
        """Clean up working directory."""
        shutil.rmtree(self.tmpdir)

    def generate(self):
        """Generate package directory tree."""
        self._generate_docs()
        self._generate_dirs()
        self._generate_files()

    def vcs_init(self):
        """Initialize VCS repository."""
        VCS(os.path.join(self.outdir, self.name), self.pkg_data)
