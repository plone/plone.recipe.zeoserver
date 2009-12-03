##############################################################################
#
# Copyright (c) 2006-2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""zeocltl -- control a ZEO server using zdaemon.

Usage: zeocltl [options] [action [arguments]]

Options:
-h/--help -- print usage message and exit
-i/--interactive -- start an interactive shell after executing commands
action [arguments] -- see below

Actions are commands like "start", "stop" and "status". If -i is
specified or no action is specified on the command line, a "shell"
interpreting actions typed interactively is started (unless the
configuration option default_to_interactive is set to false). Use the
action "help" to find out about available actions.
"""

import sys
import os

from ZEO import zeoctl
from ZEO import runzeo


if sys.platform[:3].lower() == "win":
    print 'For win32 platforms, runzeo.bat or zeoservice.exe should be used'
    print '%s is based on zdaemon, which is Linux specific' % sys.argv[0]
    print 'Aborting...'
    sys.exit(0)

def main(args=None):
    # When we detect Supervisord we need to make sure we do not fork a
    # sub process since Supervisord does not like that
    if 'SUPERVISOR_ENABLED' in os.environ:
        # We will ignore any command sent and always start in foreground mode
        args = args[:2]
        runzeo.main(args)
    else:
        zeoctl.main(args)
