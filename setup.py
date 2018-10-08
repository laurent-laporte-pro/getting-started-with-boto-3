#!/usr/bin/env python
# coding: utf-8
import io
import os
import re

from setuptools import setup

install_requires = [
    'sphinx',
    'sphinx-py3doc-enhanced-theme'
]


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(r':[a-z]+:`~?(.*?)`', r'``\1``', fd.read())


setup(
    # --- identity
    name='getting-started-with-boto-3',
    version='0.1.0',

    # --- description
    description="Getting started with Boto 3",
    long_description=u"{readme}\n{changes}".format(readme=read("README.rst"), changes=read("CHANGES.rst")),
    author=u'Laurent LAPORTE',
    author_email=u'laurent.laporte.pro@gmail.com',
    url='https://github.com/laurent-laporte-pro/getting-started-with-boto-3',
    license="MIT",
    platforms=['posix', 'nt'],
    keywords='Sphinx, Documentation, Tutorial, Amazon, S3, Glacier, AWS, Boto3, Archive',
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],

    # --- packaging
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=True,
)
