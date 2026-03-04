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
"""%(program)s -- create a ZEO instance.
Usage: %(program)s home [[host:]port] [options]

Given an "instance home directory" <home> and some configuration
options (all of which have default values), create the following:

<home>/etc/zeo.conf     -- ZEO config file
<home>/var/             -- Directory for data files: Data.fs etc.
<home>/log/             -- Directory for log files: zeo.log and zeoctl.log
<home>/bin/runzeo       -- the zeo server runner
<home>/bin/zeoctl       -- start/stop script (a shim for zeoctl.py)

Options:
    -h, --help         -- Display this help and exit
    -b, --blobs        -- Directory for Blobs. By default, it will create
                          a blobs directory at <home>/var/blobs unless a
                          path is provided -b path/to/blobs

The script will not overwrite existing files; instead, it will issue a
warning if an existing file is found that differs from the file that
would be written if it didn't exist.
"""

# WARNING!  Several templates and functions here are reused by ZRS.
# So be careful with changes.

import argparse
import os
import stat
import sys

import zdaemon
import ZODB


PROGRAM = os.path.basename(sys.argv[0])

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

ZEO_DEFAULT_BLOB_DIR = '$INSTANCE/var/blobs'


def print_(msg, *args, **kw):
    if args:
        msg = msg % args
    if kw:
        msg = msg % kw
    if not isinstance(msg, str):
        msg = msg.decode('utf8')
    sys.stdout.write('%s\n' % msg)


def usage(msg='', rc=1,
          exit=sys.exit,  # testing hook
          ):
    if not isinstance(msg, str):
        msg = str(msg)
    print_(__doc__, program=PROGRAM)
    if msg:
        print_(msg)
    exit(rc)


class ZEOInstanceBuilder:

    def get_params(self, zodb_home, zdaemon_home,
                   instance_home, address, blob_dir):
        return {
            "package": "zeo",
            "PACKAGE": "ZEO",
            "zodb_home": zodb_home,
            "zdaemon_home": zdaemon_home,
            "instance_home": instance_home,
            "blob_dir": f"blob-dir {blob_dir}" if blob_dir else "",
            "address": address,
            "python": sys.executable,
        }

    def create(self, home, params):
        makedir(home)
        makedir(home, "etc")
        makedir(home, "var")
        makedir(home, "log")
        makedir(home, "bin")

        # Create dir only when default is selected
        if ZEO_DEFAULT_BLOB_DIR in params.setdefault('blob_dir', ''):
            makedir(home, "var/blobs")

        makefile(ZEO_CONF_TEMPLATE, home, "etc", "zeo.conf", **params)
        makexfile(ZEOCTL_TEMPLATE, home, "bin", "zeoctl", **params)
        makexfile(RUNZEO_TEMPLATE, home, "bin", "runzeo", **params)

    def run(self, argv,
            usage=usage,  # testing hook
            ):

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('instance_home', nargs='?', default=None)
        parser.add_argument('addr_string', nargs='?', default='9999')
        parser.add_argument('-h', '--help', action='store_true')
        parser.add_argument('-b', '--blobs', required=False, default=None,
                            const=ZEO_DEFAULT_BLOB_DIR, nargs='?')

        parsed_args, unknown_args = parser.parse_known_args(argv)

        if len(unknown_args) > 0:
            usage(rc=1)

        if parsed_args.help:
            usage(rc=2)
        elif parsed_args.instance_home is None:
            usage(rc=1)

        instance_home = os.path.abspath(parsed_args.instance_home)

        zodb_home = os.path.split(ZODB.__path__[0])[0]
        zdaemon_home = os.path.split(zdaemon.__path__[0])[0]

        addr_string = parsed_args.addr_string

        if ':' in addr_string:
            host, port = addr_string.split(':', 1)
            address = host + ':' + port
        elif addr_string.isdigit():
            address = int(addr_string)
        else:
            usage(rc=1)

        blob_dir = parsed_args.blobs if parsed_args.blobs else None

        params = self.get_params(
            zodb_home, zdaemon_home, instance_home, address, blob_dir)
        self.create(instance_home, params)


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


def main():  # pragma: nocover
    ZEOInstanceBuilder().run(sys.argv[1:])
    print_("All done.")
