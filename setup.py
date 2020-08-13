# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import sys


version = '2.0.3'

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
    download_url='https://pypi.org/project/plone.recipe.zeoserver',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Zope Public License',
        'Framework :: Buildout',
        'Framework :: Plone',
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'Framework :: Plone :: Core',
        'Framework :: Zope',
        'Framework :: Zope :: 4',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.recipe'],
    install_requires=[
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
        'ZODB >= 5',
        'zope.mkzeoinstance >=4.1',
        'ZopeUndo',
    ] + additional_install_requires,
    extras_require={
        'zrs': ['zc.zrs']
    },
    zip_safe=False,
    entry_points={
        'zc.buildout': ['default = plone.recipe.zeoserver.recipe:Recipe'],
    },
)
