#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
changelog = open('CHANGELOG.rst').read().replace('.. :changelog:', '')

with open('requirements.txt') as f:
    required = f.read().splitlines()


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='gitlab-freak',
    version='1.0.0-alpha.1',
    description='A Flask server that allows you to interact \
        with Trello from your own Gitlab.',
    long_description=readme + '\n\n' + changelog,
    author='Michel Nemnom',
    author_email='michel.nemnom+pypi@gmail.com',
    url='https://github.com/Pegase745/gitlab-freak',
    packages=[
        'gitlab_freak',
    ],
    scripts=[
        'gitlab_freak/scripts/gitlab-freak-run.py',
        'gitlab_freak/scripts/gitlab-freak-init-db.py',
    ],
    cmdclass={'test': PyTest},
    package_dir={'gitlab_freak': 'gitlab_freak'},
    include_package_data=True,
    install_requires=required,
    license="MIT",
    zip_safe=False,
    keywords='gitlab trello',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=['pytest'],
)
