#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='shipwright_tests',
    version='0.0.1',
    packages=find_packages(include=['shipwrighttests', 'shipwrighttests.*']),
	install_requires=[
		'behave==1.2.6',
		'pyshould==0.7.1',
		'kubernetes==23.6.0',
		'pytest==7.1.2',
	],
)