# -*- coding: utf-8 -*-

import doctest
import unittest

import pkg_resources
from zc.buildout.testing import buildoutSetUp
from zc.buildout.testing import buildoutTearDown
from zc.buildout.testing import install
from zc.buildout.testing import install_develop


def setUp(test):
    buildoutSetUp(test)
    install_develop('plone.recipe.zeoserver', test)
    install('zc.recipe.egg', test)
    install('zope.mkzeoinstance', test)
    install('ZopeUndo', test)
    dependencies = pkg_resources.working_set.require('ZODB3')
    for dep in dependencies:
        try:
            install(dep.project_name, test)
        except OSError:
            # Some distribution are installed multiple times
            pass


def test_suite():
    suite = []
    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    suite.append(doctest.DocFileSuite('zeoserver.txt', optionflags=flags,
                 setUp=setUp, tearDown=buildoutTearDown))

    return unittest.TestSuite(suite)
