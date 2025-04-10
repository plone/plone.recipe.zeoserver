Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

3.0.4 (2025-03-17)
------------------

Bug fixes:


- Fix KeyError: 'zc.recipe.egg'.  [maurits] (#66)


Internal:


- Update configuration files.
  [plone devs]


3.0.3 (2025-01-23)
------------------

Tests


- Bump `macos` GHA runner version, `11` has been deprecated [@gforcada]


3.0.2 (2024-05-06)
------------------

Tests


- Removed tests for Zope Replication Services.
  The recipe support should still work, but the tests are broken.
  Note that the `zc.zrs` project is currently unmaintained, so if you rely on this, please step up.
  See `issue 52 <https://github.com/plone/plone.recipe.zeoserver/issues/52>`_.
  [maurits] (#52)


3.0.1 (2023-10-07)
------------------

Internal:


- Update configuration files.
  [plone devs] (cfffba8c)


3.0.0 (2023-05-09)
------------------

Breaking changes:


- Update Codebase to python 3.8+.
  Update required version ``zope.mkzeoinstance = 5.1.1``.
  [petschki] (#45)


Bug fixes:


- Fix lost dependencies when defining additional ``eggs`` in buildout part.
  [petschki] (#45)


2.0.3 (2020-08-14)
------------------

Bug fixes:


- Removing ZODB3_HOME variable from runzeo.bat and zeoservice.py.in files, Fix for windows machine (#41)
- fix for "ValueError: Attempted relative import in non-package" - In windows build (#42)


2.0.2 (2020-04-21)
------------------

Bug fixes:


- Minor packaging updates. (#1)


2.0.1 (2019-02-08)
------------------

Bug fixes:


- Python 3 compatibility for generated bin/zeopack script [ajung] (#36)


2.0.0 (2018-12-03)
------------------

Breaking changes:

- Drop support for ``ZODB3`` but require ``ZODB >= 5``.

New features:

- Add support for Python 3.6 and 3.7.


1.4.2 (2018-06-04)
------------------

Bug fixes:

- Move Recipe from __init__.py to a new module to get rid of the dependency on
  zc.recipe.egg in control scripts
  [tschorr]

1.4.1 (2018-02-05)
------------------

Bug fixes:

- Fixed Travis tests by installing the ``hyperlink`` package.  [maurits]

- Fixed zeopack script for ZEO >= 5 (backport from original ZEO's script) [mamico]


1.4.0 (2017-06-16)
------------------

New features:

- Requires zope.mkzeoistance > 4.0 in order to work cleanly with latest ZODB.
  [jensens]

Bug fixes:

- Cleanup: utf8 headers, isort, pep8.
  [jensens]


1.3.1 (2017-04-08)
------------------

Bug fixes:

- Fix tests to run with current Twisted version.


1.3 (2017-02-15)
----------------

New features:

- Add support for log rotation.
  [hvelarde]

Bug fixes:

- Typo in documentation. [ale-rt]


1.2.9 (2016-05-26)
------------------

Fixes:

- Updated documentation.  [mamico, gforcada]


1.2.8 (2015-04-18)
------------------

- Add default storage number in zeopack script
  [mamico]


1.2.7 (2015-01-05)
------------------

- Postpone computation of working set until recipe is ran
  [gotcha]

- Add support for initialization in main script.
  [mamico]

- Add support for Pip-installed Buildout
  [aclark]

- Add "-D" argument to zopepack options to allow override of pack days.
  [smcmahon]


1.2.6 (2013-06-04)
------------------

- add support for setting zeoserver as read only
  [vangheem]

- Add integration with ZRS
  [vangheem]


1.2.5 (2013-05-23)
------------------

- Nothing changed yet.


1.2.4 (2013-04-06)
------------------

- Adding ability to control output script name for repozo. Use the
  ``repozo-script-name`` option to change the script name.
  [do3cc]


1.2.3 (2012-10-03)
------------------

- Adding ability to control output script name for zeopack. Use the
  ``zeopack-script-name`` option to change the script name.
  [davidjb]

- Fix zeopack connection handling. The previous fix to abort after a failed
  connection attempt only worked by chance and caused zeopack to exit before
  the packing finished. Now failed connections are correctly detected and
  zeopack waits until the packing is finished.
  [gaudenz]

1.2.2 (2011-11-24)
------------------

- Fix custom zeo.conf support under windows.
  [rossp]


1.2.1 - 2011-09-12
------------------

- When the zeoserver is not running, the zeopack script cannot do
  anything.  So when zeopack cannot connect, it now quits with an
  error message.  Formerly it would wait forever.
  [maurits]

- Added 'var' option like it is in plone.recipe.zope2instance.
  [garbas]

1.2.0 - 2010-10-18
------------------

- Only require a ``nt_svcutils`` distribution on Windows.
  [hannosch]

1.1.1 - 2010-07-20
------------------

- Fixed -B option being required for along with the -S option.
  [vangheem]

- Added documentation for using the zeopack script with mount points.
  [vangheem]

1.1 - 2010-07-18
----------------

- No changes.

1.1b1 - 2010-07-02
------------------

- Implemented Windows support and support for running ZEO as a Windows service.
  We depend on the new nt_svcutils distribution to provide this support.
  [baijum, hannosch]

- The FileStorage component of ZODB 3.9 now supports blobs natively,
  so no need to use BlobStorage proxy for it anymore.
  [baijum, hannosch]

- Added ``extra-paths`` option to add additional modules paths.
  [baijum]

- Fixed ZEO packing of mounted storage.
  [vangheem]

- Added -B option to the ``zeopack`` script to specify the location of the
  blob storage.
  [vangheem]

1.1a2 - 2010-05-10
------------------

- Added support for the ``pack-keep-old`` option introduced in ZODB 3.9.
  [hannosch]

1.1a1 - 2010-04-27
------------------

- Added support for the ``pack-gc`` option introduced in ZODB 3.9.
  [hannosch]

- Always create a blob-storage by default.
  [hannosch]

- Require at least ZODB 3.8 and simplify the ``zeopack`` script.
  [hannosch]

- Various documentation updates.
  [hannosch]

- Use the new ``zope.mkzeoinstance`` package, which makes the recipe compatible
  with ZODB 3.9.5+.
  [hannosch]

- Removed unmaintained win32 specific tests and old zope2 test mockups.
  [hannosch]

- Removed testing dependency on ``zope.testing`` and refactored testing setup.
  [hannosch]

1.0 - 2010-04-05
----------------

- Depend on and always include ZopeUndo. While it's only needed for Zope 2, the
  distribution is so tiny, it doesn't hurt for non-Zope 2 ZEO servers.
  [hannosch]

1.0b1 - 2010-03-19
------------------

- Fixed issue with egg paths for the zeopack script.
  [davisagli]

- Added support for setting ZEO log level.
  [baijum]

1.0a2 - 2009-12-03
------------------

* Set up logging configuration that is needed by ZODB.blob.
  [davisagli]

* Set shared_blob_dir to True when initializing the ClientStorage used
  by the pack script, since it will be using the same blob directory
  as the ZEO server.
  [davisagli]

1.0a1 - 2009-12-03
------------------

* Updated and cleaned up after renaming.
  [hannosch]

* Added compatibility with eggified Zopes (Zope >= 2.12).
  [davisagli]

* Initial implementation based on plone.recipe.zope2zeoserver.
  [plone]
