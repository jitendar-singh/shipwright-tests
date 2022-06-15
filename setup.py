#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='shipwright_tests',
    version='0.0.1',
    packages=find_packages(include=['shipwrighttests', 'shipwrighttests.*']),
	install_requires=[
		'behave==1.2.6',
		'kubernetes==23.6.0',
	],
)