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
    version='0.1.0',
    description='Python Boilerplate contains all the boilerplate you need to create a Python package.',
    long_description=readme + '\n\n' + history,
    author='Bo Lopker',
    author_email='blopker@23andme.com',
    url='https://github.com/blopker/djdt_flamegraph',
    packages=[
        'djdt_flamegraph',
    ],
    package_dir={'djdt_flamegraph':
                 'djdt_flamegraph'},
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    keywords='djdt_flamegraph',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
)
