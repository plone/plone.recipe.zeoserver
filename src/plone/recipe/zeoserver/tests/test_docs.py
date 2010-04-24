# -*- coding: utf-8 -*-

import doctest
import unittest
import os

from zc.buildout.testing import buildoutSetUp
from zc.buildout.testing import buildoutTearDown
from zc.buildout.testing import install
from zc.buildout.testing import install_develop

current_dir = os.path.abspath(os.path.dirname(__file__))


def setUp(test):
    buildoutSetUp(test)
    install_develop('plone.recipe.zeoserver', test)
    install('transaction', test)
    install('ZConfig', test)
    install('ZODB3', test)
    install('ZopeUndo', test)
    install('zc.lockfile', test)
    install('zc.recipe.egg', test)
    install('zdaemon', test)
    install('zope.event', test)
    install('zope.exceptions', test)
    install('zope.interface', test)
    install('zope.proxy', test)


def test_suite():
    suite = []
    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    # filtering files on extension
    docs = [os.path.join(current_dir, doc) for doc in
            os.listdir(current_dir) if doc.endswith('.txt')]

    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags,
                    setUp=setUp, tearDown=buildoutTearDown,
                    module_relative=False))

    return unittest.TestSuite(suite)
