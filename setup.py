#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='djdt_flamegraph',
    version='0.2.5',
    description='Flamegraphs for Django Debug Toolbar',
    long_description=readme + '\n\n' + history,
    author='Bo Lopker',
    author_email='blopker@23andme.com',
    url='https://github.com/23andme/djdt-flamegraph',
    packages=[
        'djdt_flamegraph',
    ],
    package_dir={'djdt_flamegraph':
                 'djdt_flamegraph'},
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    keywords='djdt_flamegraph',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
)
