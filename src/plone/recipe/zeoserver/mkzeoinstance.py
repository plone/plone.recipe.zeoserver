##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
# This file was originally copied on 2026-03-04 from zope.mkzeoinstance 6.0.
# See https://github.com/plone/plone.recipe.zeoserver/issues/91
#
##############################################################################

# WARNING!  Several templates and functions here are reused by ZRS.
# So be careful with changes.  But ZRS is unmaintainted anyway.

import os
import stat
import sys

ZEO_CONF_TEMPLATE = """\
# ZEO configuration file

%%define INSTANCE %(instance_home)s

<zeo>
  address %(address)s
  read-only false
  invalidation-queue-size 100
  # pid-filename $INSTANCE/var/ZEO.pid
  # monitor-address PORT
  # transaction-timeout SECONDS
</zeo>

<filestorage 1>
  path $INSTANCE/var/Data.fs
  %(blob_dir)s
</filestorage>

<eventlog>
  level info
  <logfile>
    path $INSTANCE/log/zeo.log
  </logfile>
</eventlog>

<runner>
  program $INSTANCE/bin/runzeo
  socket-name $INSTANCE/var/%(package)s.zdsock
  daemon true
  forever false
  backoff-limit 10
  exit-codes 0, 2
  directory $INSTANCE
  default-to-interactive true
  # user zope
  python %(python)s
  zdrun %(zdaemon_home)s/zdaemon/zdrun.py

  # This logfile should match the one in the %(package)s.conf file.
  # It is used by zdctl's logtail command, zdrun/zdctl doesn't write it.
  logfile $INSTANCE/log/%(package)s.log
</runner>
"""


ZEOCTL_TEMPLATE = """\
#!/bin/sh
# %(PACKAGE)s instance control script

# The following two lines are for chkconfig.  On Red Hat Linux (and
# some other systems), you can copy or symlink this script into
# /etc/rc.d/init.d/ and then use chkconfig(8) to automatically start
# %(PACKAGE)s at boot time.

# chkconfig: 345 90 10
# description: start a %(PACKAGE)s server

PYTHON="%(python)s"
INSTANCE_HOME="%(instance_home)s"
ZODB3_HOME="%(zodb_home)s"

CONFIG_FILE="%(instance_home)s/etc/%(package)s.conf"

PYTHONPATH="$ZODB3_HOME"
export PYTHONPATH INSTANCE_HOME

exec "$PYTHON" -m ZEO.zeoctl -C "$CONFIG_FILE" ${1+"$@"}
"""


RUNZEO_TEMPLATE = """\
#!/bin/sh
# %(PACKAGE)s instance start script

PYTHON="%(python)s"
INSTANCE_HOME="%(instance_home)s"
ZODB3_HOME="%(zodb_home)s"

CONFIG_FILE="%(instance_home)s/etc/%(package)s.conf"

PYTHONPATH="$ZODB3_HOME"
export PYTHONPATH INSTANCE_HOME

exec "$PYTHON" -m ZEO.runzeo -C "$CONFIG_FILE" ${1+"$@"}
"""

ZEO_DEFAULT_BLOB_DIR = "$INSTANCE/var/blobs"


def print_(msg, *args, **kw):
    if args:
        msg = msg % args
    if kw:
        msg = msg % kw
    if not isinstance(msg, str):
        msg = msg.decode("utf8")
    sys.stdout.write("%s\n" % msg)


class ZEOInstanceBuilder:

    def create(self, home, params):
        makedir(home)
        makedir(home, "etc")
        makedir(home, "var")
        makedir(home, "log")
        makedir(home, "bin")

        # Create dir only when default is selected
        if ZEO_DEFAULT_BLOB_DIR in params.setdefault("blob_dir", ""):
            makedir(home, "var/blobs")

        makefile(ZEO_CONF_TEMPLATE, home, "etc", "zeo.conf", **params)
        makexfile(ZEOCTL_TEMPLATE, home, "bin", "zeoctl", **params)
        makexfile(RUNZEO_TEMPLATE, home, "bin", "runzeo", **params)


def makedir(*args):
    path = ""
    for arg in args:
        path = os.path.join(path, arg)
    mkdirs(path)
    return path


def mkdirs(path):
    if os.path.isdir(path):
        return
    head, tail = os.path.split(path)
    if head and tail and not os.path.isdir(head):
        mkdirs(head)
    os.mkdir(path)
    print_("Created directory %s", path)


def makefile(template, *args, **kwds):
    path = makedir(*args[:-1])
    path = os.path.join(path, args[-1])
    data = template % kwds
    if os.path.exists(path):
        with open(path) as f:
            olddata = f.read().strip()
        if olddata:
            if olddata != data.strip():
                print_("Warning: not overwriting existing file %s", path)
            return path
    with open(path, "w") as f:
        f.write(data)
    print_("Wrote file %s", path)
    return path


def makexfile(template, *args, **kwds):
    path = makefile(template, *args, **kwds)
    umask = os.umask(0o022)
    os.umask(umask)
    mode = 0o0777 & ~umask
    if stat.S_IMODE(os.stat(path)[stat.ST_MODE]) != mode:
        os.chmod(path, mode)
        print_("Changed mode for %s to %o", path, mode)
    return path
