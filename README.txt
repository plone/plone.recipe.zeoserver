plone.recipe.zeoserver
======================

This recipe creates and configures a ZEO server in parts. It also
installs a control script, which is like zeoctl, in the bin/ directory.
The name of the control script is the the name of the part in buildout.

You can use it with a part like this::

  [zeoserver]
  recipe = plone.recipe.zeoserver
  zeo-address = 8100

Options
-------

zeopack
  The path to the zeopack.py backup script. A wrapper for this will be
  generated in bin/zeopack, which sets up the appropriate environment to
  run this. Defaults to using the zeopack script from the ZODB3 egg.
  Set this option to an empty value if you do not want this script to be
  generated.

repozo
  The path to the repozo.py backup script. A wrapper for this will be
  generated in bin/repozo, which sets up the appropriate environment for
  running this. Defaults to using the repozo script from the ZODB3 egg.
  Set this to an empty value if you do not want this script to be generated.

zeo-conf
  A relative or absolute path to a zeo.conf file. If this is not given, a
  zeo.conf will be generated based on the the options below.

The following options all affect the generated zope.conf.

zeo-address
  Give a port for the ZEO server (either specify the port number only (with
  'localhost' as default) or you use the format ``host:port``). Defaults to 8100.

effective-user
  The name of the effective user for the ZEO process. Defaults to not setting
  an effective user.

invalidation-queue-size
  The invalidation-queue-size used for the ZEO server. Defaults to 100.

zeo-log
  The filename of the ZEO log file. Defaults to var/log/${partname}.log

zeo-log-format
  Format of logfile entries. Defaults to %(asctime)s %(message)s

zeo-log-custom
  A custom section for the eventlog, to be able to use another
  event logger than `logfile`. `zeo-log` is still used to set the logfile
  value in the runner section.

storage-number
  The number used to identify a storage.

file-storage
  The filename where the ZODB data file will be stored.
  Defaults to var/filestorage/Data.fs.

blob-storage
  The folder where the ZODB blob data files will be stored.

socket-name
  The filename where ZEO will write its socket file.
  Defaults to var/zeo.zdsock.

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
  The authentication realm. Defaults to 'ZEO'

pack-days
  Specify of days for the zeopack script to retain of history. Defaults to
  one day.

pack-user
  If the ZEO server uses authentication, this is the username used by the
  zeopack script to connect to the ZEO server.

pack-password
  If the ZEO server uses authentication, this is the password used by the
  zeopack script to connect to the ZEO server.

zeo-conf-additional
  Give additional lines to zeo.conf. Make sure you indent any lines after
  the one with the parameter.

monitor-address
  The address at which the monitor server should listen.
  The monitor server provides server statistics in a simple text format.

relative-paths
  Set this to `true` to make the generated scripts use relative
  paths. You can also enable this in the `[buildout]` section.

eggs
  Set if you need to include other packages as eggs e.g. for making
  application code available on the ZEO server side for performing
  conflict resolution (through the _p_resolveConflict() handler).

Reporting bugs or asking questions
----------------------------------

We have a shared bugtracker and help desk on Launchpad:
https://bugs.launchpad.net/collective.buildout/
