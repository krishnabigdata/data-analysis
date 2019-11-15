#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name='taxi-data-analaysis',
    version='1.0.0',

    description='taxi data analysis Python project',
    long_description=open('README.md', encoding="utf-8").read(),
    keywords=['python'],

    author='Krishna',
    url='https://github.com/krishnabigdata/taxi-data-analysis',

    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=open('requirements.txt').readlines(),
    zip_safe=False,
    entry_points={
        'console_scripts': ['processing=processing.cli:main'],
    }
)
