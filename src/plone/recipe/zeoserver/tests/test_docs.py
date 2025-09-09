from zc.buildout.testing import buildoutSetUp
from zc.buildout.testing import buildoutTearDown
from zc.buildout.testing import install
from zc.buildout.testing import install_develop

import doctest
import shutil
import unittest


def setUp(test):
    buildoutSetUp(test)
    install_develop("plone.recipe.zeoserver", test)
    install("zc.recipe.egg", test)
    install("zope.mkzeoinstance", test)
    install("ZopeUndo", test)
    install("zc.zrs", test)
    install("Automat", test)
    install("incremental", test)
    install("constantly", test)
    install("attrs", test)
    install("Twisted", test)
    install("hyperlink", test)
    install("idna", test)


def tearDown(test):
    buildoutTearDown(test)
    sample_buildout = test.globs["sample_buildout"]
    shutil.rmtree(sample_buildout, ignore_errors=True)


def test_suite():
    suite = []
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

    suite.append(
        doctest.DocFileSuite(
            "zeoserver.txt", optionflags=flags, setUp=setUp, tearDown=buildoutTearDown
        )
    )

    return unittest.TestSuite(suite)
