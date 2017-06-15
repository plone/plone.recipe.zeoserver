# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import sys


version = '1.4.0'

additional_install_requires = []

if sys.platform[:3].lower() == 'win':
    additional_install_requires += ['nt_svcutils']


setup(
    name="plone.recipe.zeoserver",
    version=version,
    author='Hanno Schlichting',
    author_email='hannosch@plone.org',
    description='ZC Buildout recipe for installing a ZEO server',
    long_description=(
        open('README.rst').read() +
        '\n' +
        open('CHANGES.rst').read()
    ),
    license='ZPL 2.1',
    keywords='zope2 zeo zodb buildout',
    url='https://github.com/plone/plone.recipe.zeoserver',
    download_url='https://pypi.python.org/pypi/plone.recipe.zeoserver',
    classifiers=[
        'License :: OSI Approved :: Zope Public License',
        'Framework :: Buildout',
        'Framework :: Zope2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.recipe'],
    install_requires=[
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
        'ZODB3 >= 3.8',
        'zope.mkzeoinstance >=4',
        'ZopeUndo',
    ] + additional_install_requires,
    extras_require={
        'zrs': ['zc.zrs']
    },
    zip_safe=False,
    entry_points={
        'zc.buildout': ['default = plone.recipe.zeoserver:Recipe'],
    },
)
