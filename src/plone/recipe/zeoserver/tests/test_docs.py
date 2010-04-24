# -*- coding: utf-8 -*-

import doctest
import unittest
import os

import zc.buildout.testing, zc.buildout.easy_install

current_dir = os.path.abspath(os.path.dirname(__file__))


def test_suite():
    suite = []
    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    # filtering files on extension
    docs = [os.path.join(current_dir, doc) for doc in
            os.listdir(current_dir) if doc.endswith('.txt')]

    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags,
                    setUp=zc.buildout.testing.buildoutSetUp,
                    tearDown=zc.buildout.testing.buildoutTearDown,
                    module_relative=False))

    return unittest.TestSuite(suite)
