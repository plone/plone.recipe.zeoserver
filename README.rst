Overview
========

This recipe creates and configures a ZEO server in parts. It also installs a
control script in the bin/ directory. The name of the control script is the
name of the part in buildout.

You can use it with a part like this::

  [zeo]
  recipe = plone.recipe.zeoserver
  zeo-address = 8100

This will create a control script ``bin/zeo``.

You can either start the database in foreground mode via ``bin/zeo fg`` or use
the built-in zdaemon process control and use the ``start/stop/restart/status``
commands. The foreground mode is suitable for running the process under general
process control software like supervisord.

Note: Windows support for this recipe is currently limited.

Options
-------

The following options all affect the generated zeo.conf. If you want to have
full control over the configuration file, see the ``zeo-conf`` option in the
advanced options.

Process
-------

zeo-address
  Give a port for the ZEO server (either specify the port number only (with
  '127.0.0.1' as default) or you use the format ``host:port``).
  Defaults to ``8100``.

effective-user
  The name of the effective user for the ZEO process. Defaults to not setting
  an effective user. This causes the process to run under the user account the
  process has been started with.

socket-name
  The filename where ZEO will write its socket file.
  Defaults to ``var/zeo.zdsock``.

Storage
-------

storage-number
  The number used to identify a storage. Defaults to ``1``.

file-storage
  The filename where the ZODB data file will be stored.
  Defaults to ``var/filestorage/Data.fs``.

blob-storage
  The folder where the ZODB blob data files will be stored.
  Defaults to ``var/blobstorage``.

Logging
-------

zeo-log
  The filename of the ZEO log file. Defaults to ``var/log/${partname}.log``.

zeo-log-level
  Control the logging level in the eventlog. Defaults to ``info``.

zeo-log-max-size
  Maximum size of ZEO log file. Enables log rotation.

zeo-log-old-files
  Number of previous log files to retain when log rotation is enabled. Defaults to ``1``.

zeo-log-format
  Format of logfile entries. Defaults to ``%(asctime)s %(message)s``.

zeo-log-custom
  A custom section for the eventlog, to be able to use another
  event logger than ``logfile``. ``zeo-log`` is still used to set the logfile
  value in the runner section.

Authentication
--------------

authentication-database
  The filename for a authentication database. Only accounts listed in this
  database will be allowed to access the ZEO server.

  The format of the database file is::

    realm <realm>
    <username>:<hash>

  Where the hash is generated via::

    import sha
    string = "%s:%s:%s" % (username, realm, password)
    sha.new(string).hexdigest()

authentication-realm
  The authentication realm. Defaults to ``ZEO``.

Packing
-------

pack-days
  How many days of history should the zeopack script retain. Defaults to
  one day.

pack-gc
  Can be set to ``false`` to disable garbage collection as part of the pack.
  Defaults to ``true``.

pack-keep-old
  Can be set to ``false`` to disable the creation of ``*.fs.old`` files before
  the pack is run. Defaults to ``true``.

pack-user
  If the ZEO server uses authentication, this is the username used by the
  zeopack script to connect to the ZEO server.

pack-password
  If the ZEO server uses authentication, this is the password used by the
  zeopack script to connect to the ZEO server.


ZRS
---

First off, you'll need to specify the recipe to install zc.zrs. To do so,
just slightly change the way the recipe option is specified in your zeoserver
buildout part::

    [zeoserver]
    recipe = plone.recipe.zeoserver[zrs]
    ...


replicate-to
    host:port combination this ZRS should liston to as a primary.
    ZRS Secondaries connect here to get replication data.

replicate-from
    host:port combination of a ZRS primary this ZRS should connect to as a secondary.
    This ZRS replicates the data it gets from the primary.

keep-alive-delay
    In some network configurations, TCP connections are broken after extended
    periods of inactivity. This may even be done in a way that a client doesn't
    detect the disconnection. To prevent this, you can use the keep-alive-delay
    option to cause the secondary storage to send periodic no-operation
    messages to the server.


Monitoring
----------

monitor-address
  The address at which the monitor server should listen. The monitor server
  provides server statistics in a simple text format.

Performance
-----------

invalidation-queue-size
  The invalidation-queue-size used for the ZEO server. Defaults to ``100``.

Customization
-------------

var
  Used to configure the base directory for all things going into var.
  Defaults to ${buildout:directory}/var.

zeo-conf-additional
  Give additional lines to zeo.conf. Make sure you indent any lines after
  the one with the parameter. This allows you to use generated zeo.conf file
  but add some minor additional lines to it.

eggs
  Set if you need to include other packages as eggs e.g. for making
  application code available on the ZEO server side for performing
  conflict resolution (through the _p_resolveConflict() handler).

extra-paths
  Specify additional directories which should be available to the control
  scripts. Use this only for non-eggified Python packages.

zeo-conf
  A relative or absolute path to a zeo.conf file. This lets you provide a
  completely custom configuration file and ignore most of the options in
  this recipe.

repozo
  The path to the repozo.py backup script. A wrapper for this will be
  generated in bin/repozo, which sets up the appropriate environment for
  running this. Defaults to using the repozo script from the ZODB3 egg.
  Set this to an empty value if you do not want this script to be generated.

repozo-script-name
  The name of the wrapper script to generate in `bin/`. Defaults to `repozo`.
  Change this option if you have more than one instance of this recipe in
  the one buildout to create separate scripts and avoid any one script being
  overwritten.

zeopack
  The path to the zeopack.py backup script. A wrapper for this will be
  generated in bin/zeopack (unless you change `zeopack-script-name`), which
  sets up the appropriate environment to run this. Defaults to using the zeopack
  script from the ZODB3 egg.  Set this option to an empty value if you do not
  want this script to be generated.

zeopack-script-name
  The name of the wrapper script to generate in `bin/`. Defaults to `zeopack`.
  Change this option if you have more than one instance of this recipe in
  the one buildout to create separate scripts and avoid any one script being
  overwritten.

relative-paths
  Set this to `true` to make the generated scripts use relative
  paths. You can also enable this in the `[buildout]` section.

read-only
  Set zeoserver to run in read-only mode


Usage
-----

zeopack
  A zeopack script will be generated for you in the buildout bin directory,
  unless you change the `zeopack-script-name` option, in which case the script
  will be called the name you specify. If you'd like to use this script to pack
  a different mount point, you'll need to specify `-S mount_name`. You can also
  specify a `-B` option to not use the default blob directory.
  You may override the pack-days by adding "-D #" to the command line where
  "#" is the number of days to keep.


Reporting bugs or asking questions
----------------------------------

We have a bugtracker and help desk on Github:
https://github.com/plone/plone.recipe.zeoserver/issues
