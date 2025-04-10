import logging
import os
import shutil
import sys
import zc.buildout
import zc.recipe.egg


try:
    import zc.zrs

    HAS_ZRS = True
except ImportError:
    HAS_ZRS = False
join = os.path.join

curdir = os.path.dirname(__file__)


class Recipe:
    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options["recipe"], options)
        self.buildout, self.options, self.name = buildout, options, name

        if self.options.get("eggs") and options["recipe"] not in self.options["eggs"]:
            # make sure we do not loose our own dependencies if additional eggs are provided
            self.options["eggs"] += "\n%s" % options["recipe"]

        options["location"] = os.path.join(
            buildout["buildout"]["parts-directory"],
            self.name,
        )
        options["bin-directory"] = buildout["buildout"]["bin-directory"]
        options["scripts"] = ""  # suppress script generation.

        # Relative path support for the generated scripts
        relative_paths = options.get(
            "relative-paths", buildout["buildout"].get("relative-paths", "false")
        )
        if relative_paths == "true":
            options["buildout-directory"] = buildout["buildout"]["directory"]
            self._relative_paths = options["buildout-directory"]
        else:
            self._relative_paths = ""
            assert relative_paths == "false"

    _ws_locations = None

    @property
    def ws_locations(self):
        if self._ws_locations is None:
            self._ws_locations = {d.location for d in self.zodb_ws}
        return self._ws_locations

    def install(self):
        _, self.zodb_ws = self.egg.working_set()

        options = self.options
        location = options["location"]

        if os.path.exists(location):
            shutil.rmtree(location)

        self.module_paths = self.options.get("extra-paths", [])
        if self.module_paths:
            # Filter out empty directories
            self.module_paths = [p for p in self.module_paths.split("\n") if p]

        # this was taken from mkzeoinstance.py
        import zdaemon

        zdaemon_home = os.path.split(zdaemon.__path__[0])[0]

        import ZEO

        self.zodb_home = os.path.dirname(os.path.dirname(ZEO.__file__))
        params = {
            "package": "zeo",
            "PACKAGE": "ZEO",
            "zodb_home": self.zodb_home,
            "zdaemon_home": zdaemon_home,
            "instance_home": location,
            "address": "8100",  # will be overwritten later
            "python": options["executable"],
        }
        from zope.mkzeoinstance import ZEOInstanceBuilder

        ZEOInstanceBuilder().create(location, params)

        try:
            # Save the working set:
            open(os.path.join(location, "etc", ".eggs"), "w").write(
                "\n".join(self.ws_locations)
            )

            # Make a new zeo.conf based on options in buildout.cfg
            self.build_zeo_conf()

            # Patch extra paths into binaries
            self.patch_binaries()

            # Install extra scripts
            self.install_scripts()

        except Exception:  # clean up
            shutil.rmtree(location)
            raise

        return location

    def update(self):
        _, self.zodb_ws = self.egg.working_set()

        options = self.options
        location = options["location"]

        if os.path.exists(location):
            # See if we can stop. We need to see if the working set path
            # has changed.
            saved_path = os.path.join(location, "etc", ".eggs")
            if os.path.isfile(saved_path):
                if open(saved_path).read() != "\n".join(self.ws_locations):
                    # Something has changed. Blow away the instance.
                    self.install()

            # Nothing has changed.
            return location

        else:
            self.install()

        return location

    def build_zeo_conf(self):
        """Create a zeo.conf file"""
        options = self.options
        location = options["location"]
        instance_home = location

        base_dir = self.buildout["buildout"]["directory"]
        var_dir = options.get("var", os.path.join(base_dir, "var"))
        if not os.path.exists(var_dir):
            os.makedirs(var_dir)

        self.pid_file = options.get(
            "pid-file", os.path.join(var_dir, self.name + ".pid")
        )

        zeo_conf_path = options.get("zeo-conf", None)
        if zeo_conf_path is not None:
            zeo_conf = "%%include %s" % os.path.abspath(zeo_conf_path)
        else:
            zeo_address = options.get("zeo-address", "8100")
            zeo_conf_additional = options.get("zeo-conf-additional", "")
            storage_number = options.get("storage-number", "1")

            monitor_address = options.get("monitor-address", "")
            if monitor_address:
                monitor_address = "monitor-address %s" % monitor_address

            effective_user = options.get("effective-user", "")
            if effective_user:
                effective_user = "user %s" % effective_user

            invalidation_queue_size = options.get("invalidation-queue-size", "100")

            socket_name = options.get("socket-name", "%s/zeo.zdsock" % var_dir)
            socket_dir = os.path.dirname(socket_name)
            if not os.path.exists(socket_dir):
                os.makedirs(socket_dir)

            z_log_name = os.path.sep.join(("log", self.name + ".log"))
            zeo_log_level = options.get("zeo-log-level", "info")
            zeo_log_custom = options.get("zeo-log-custom", None)

            # if zeo-log is given, we use it to set the runner
            # logfile value in any case
            z_log_filename = options.get("zeo-log", z_log_name)
            z_log_filename = os.path.join(var_dir, z_log_filename)
            z_log_dir = os.path.dirname(z_log_filename)
            if not os.path.exists(z_log_dir):
                os.makedirs(z_log_dir)

            # zeo-log-custom supersedes zeo-log
            logformat = options.get("zeo-log-format", "%(asctime)s %(message)s")
            if zeo_log_custom is None:
                zeo_log_rotate = ""
                zeo_log_max_size = options.get("zeo-log-max-size", None)
                if zeo_log_max_size:
                    zeo_log_old_files = options.get("zeo-log-old-files", 1)
                    zeo_log_rotate = "\n".join(
                        (
                            "max-size %s" % zeo_log_max_size,
                            "      old-files %s" % zeo_log_old_files,
                        )
                    )
                z_log = z_log_file % {
                    "filename": z_log_filename,
                    "logformat": logformat,
                    "zeo_log_rotate": zeo_log_rotate,
                }
            else:
                z_log = zeo_log_custom

            file_storage = os.path.sep.join(("filestorage", "Data.fs"))
            file_storage = options.get("file-storage", file_storage)
            file_storage = os.path.join(var_dir, file_storage)
            file_storage_dir = os.path.dirname(file_storage)
            if not os.path.exists(file_storage_dir):
                os.makedirs(file_storage_dir)

            if options.get("authentication-database", ""):
                authentication = authentication_template % dict(
                    database=options.get("authentication-database"),
                    realm=options.get("authentication-realm", "ZEO"),
                )
            else:
                authentication = ""

            blob_storage = options.get("blob-storage", "blobstorage")
            if blob_storage:
                blob_storage = os.path.join(var_dir, blob_storage)
                storage_template = blob_storage_template
            else:
                storage_template = file_storage_template

            effective_user = options.get("effective-user", "")
            if effective_user:
                effective_user = "user %s" % effective_user

            pack_gc = options.get("pack-gc", "")
            if pack_gc.lower() == "false":
                pack_gc = "pack-gc false"

            pack_keep_old = options.get("pack-keep-old", "")
            if pack_keep_old.lower() == "false":
                pack_keep_old = "pack-keep-old false"

            storage = storage_template % dict(
                storage_number=storage_number,
                file_storage=file_storage,
                blob_storage=blob_storage,
                pack_gc=pack_gc,
                pack_keep_old=pack_keep_old,
            )

            # ZRS config
            rfrom = options.get("replicate-from")
            rto = options.get("replicate-to")
            if HAS_ZRS and (rfrom or rto):
                replicate = ""
                if rfrom:
                    replicate += "\nreplicate-from %s" % rfrom
                if rto:
                    replicate += "\nreplicate-to %s" % rto
                keep_alive = options.get("keep-alive-delay", "60")
                storage = zrs_template % dict(
                    storage=storage,
                    keep_alive=keep_alive,
                    replicate=replicate,
                    storage_number=storage_number,
                )

            read_only = options.get("read-only", "false")
            zeo_conf = zeo_conf_template % dict(
                instance_home=instance_home,
                effective_user=effective_user,
                invalidation_queue_size=invalidation_queue_size,
                socket_name=socket_name,
                z_log=z_log,
                z_log_filename=z_log_filename,
                authentication=authentication,
                storage=storage,
                zeo_address=zeo_address,
                pid_file=self.pid_file,
                zeo_conf_additional=zeo_conf_additional,
                monitor_address=monitor_address,
                zeo_log_level=zeo_log_level,
                read_only=read_only,
            )

        zeo_conf_path = os.path.join(location, "etc", "zeo.conf")
        open(zeo_conf_path, "w").write(zeo_conf)

    def patch_binaries(self):
        location = self.options["location"]
        # XXX We need to patch the windows specific batch scripts
        # and they need a different path separator
        path = (
            os.path.pathsep.join(self.ws_locations)
            + os.path.pathsep
            + os.path.pathsep.join(self.module_paths)
        )
        for script_name in ("runzeo", "zeoctl"):
            script_path = os.path.join(location, "bin", script_name)
            script = open(script_path).read()
            script = script.replace(
                'PYTHONPATH="$ZODB3_HOME"', 'PYTHONPATH="%s"' % path
            )
            f = open(script_path, "w")
            f.write(script)
            f.close()

    def install_scripts(self):
        options = self.options
        location = options["location"]

        self.zeo_conf = options.get("zeo-conf", None)
        if self.zeo_conf is None:
            self.zeo_conf = os.path.join(location, "etc", "zeo.conf")

        _, ws = self.egg.working_set(["plone.recipe.zeoserver"])

        zc.buildout.easy_install.scripts(
            [(self.name, "plone.recipe.zeoserver.ctl", "main")],
            ws,
            options["executable"],
            options["bin-directory"],
            initialization=options.get("initialization", ""),
            arguments=(
                '\n        ["-C", %r]' "\n        + sys.argv[1:]" % self.zeo_conf
            ),
            extra_paths=self.module_paths,
            relative_paths=self._relative_paths,
        )

        # zeopack.py
        zeopack = options.get("zeopack", None)
        zeopack_script_name = options.get("zeopack-script-name", "zeopack")
        zeopack_scripts = dict(zeopack=zeopack_script_name)
        if zeopack is not None:
            directory, filename = os.path.split(zeopack)
            if zeopack and os.path.exists(zeopack):
                zc.buildout.easy_install.scripts(
                    [("zeopack", os.path.splitext(filename)[0], "main")],
                    ws,
                    options["executable"],
                    options["bin-directory"],
                    scripts=zeopack_scripts,
                    extra_paths=ws + [directory] + self.module_paths,
                    relative_paths=self._relative_paths,
                )
        else:
            host = port = socket_path = ""
            zeo_address = options.get("zeo-address", "8100")
            parts = zeo_address.split(":")

            if len(parts) == 1:
                try:
                    # if the only argument is a port, which must be an int,
                    # we use 127.0.0.1 as the host by default
                    port = int(zeo_address)
                except ValueError:
                    # The address is a simple string, we now assume it is
                    # a path to a Unix socket file
                    socket_path = zeo_address
                else:
                    host = "127.0.0.1"
                    port = zeo_address
            else:
                host, port = parts

            username = options.get("pack-user", None)
            password = options.get("pack-password", None)
            if username is not None:
                realm = options.get("authentication-realm", "ZEO")
            else:
                realm = None
            storage = options.get("storage-number", "1")

            arg_list = [
                "host",
                "port",
                "unix",
                "days",
                "username",
                "password",
                "realm",
                "blob_dir",
                "storage",
            ]
            arguments = dict(
                address=zeo_address,
                host=host,
                port=port,
                unix=socket_path,
                days=options.get("pack-days", 1),
                username=username,
                password=password,
                realm=realm,
                storage=storage,
                blob_dir=options.get("blob-storage", None),
            )
            arguments_info = ""
            for k, v in arguments.items():
                if not v:
                    arguments_info += "%s = None\n" % k
                else:
                    arguments_info += f'{k} = "{v}"\n'

            arguments_info += (
                "import getopt; opts = "
                "getopt.getopt(sys.argv[1:], 'S:B:D:W1')[0];\n"
                "opts = dict(opts)\n"
                "storage = opts.get('-S') and "
                "opts['-S'] or storage\n"
                "blob_dir = opts.get('-B') and "
                "opts['-B'] or blob_dir\n"
                "days = opts.get('-D') and "
                "opts['-D'] or days\n"
            )

            # Make sure the recipe itself and its dependencies are on the path
            extra_paths = [ws.by_key[options["recipe"].replace("[zrs]", "")].location]
            for package_name in ("zc.buildout", "zc.recipe.egg"):
                # This may fail if Buildout installed with Pip.  Or we may just need
                # to query by a different name.
                try:
                    extra_paths.append(ws.by_key[package_name].location)
                except KeyError:
                    package_name = package_name.replace(".", "-")
                    try:
                        extra_paths.append(ws.by_key[package_name].location)
                    except KeyError:
                        pass
            zc.buildout.easy_install.scripts(
                [("zeopack", "plone.recipe.zeoserver.pack", "main")],
                self.zodb_ws,
                options["executable"],
                options["bin-directory"],
                scripts=zeopack_scripts,
                initialization=arguments_info,
                arguments=", ".join(arg_list),
                relative_paths=self._relative_paths,
                extra_paths=extra_paths + self.module_paths,
            )

        # The backup script, pointing to repozo.py
        repozo = options.get("repozo", None)
        repozo_script_name = options.get("repozo-script-name", "repozo")
        repozo_scripts = dict(repozo=repozo_script_name)
        if repozo is None:
            repozo = "ZODB.scripts.repozo"
            extra_paths = []
        else:
            if not os.path.exists(repozo):
                raise AssertionError("Custom repozo script not found: %s" % repozo)
            directory, filename = os.path.split(repozo)
            repozo = os.path.splitext(filename)[0]
            extra_paths = [directory]
        zc.buildout.easy_install.scripts(
            [("repozo", repozo, "main")],
            self.zodb_ws,
            options["executable"],
            options["bin-directory"],
            scripts=repozo_scripts,
            extra_paths=extra_paths + self.module_paths,
            relative_paths=self._relative_paths,
        )

        if sys.platform == "win32":
            self.install_win32_scripts()

    def install_win32_scripts(self):
        path = list(self.ws_locations) + self.module_paths
        location = self.options["location"]

        arguments = {
            "PYTHON": self.options["executable"],
            "zodb_home": self.zodb_home,
            "INSTANCE_HOME": location,
            "PYTHONPATH": os.path.pathsep.join(path),
            "PACKAGE": "zeo",
            "PID_FILENAME": self.pid_file,
        }

        # runzeo.bat
        runzeo_filename = "%s_runzeo.bat" % self.name
        runzeo = open(join(curdir, "runzeo.bat")).read()
        self._write_file(
            os.path.join(self.options["bin-directory"], runzeo_filename),
            runzeo % arguments,
        )

        # zeoservice.py
        zeo_filename = "%s_service" % self.name
        zeo_service = open(join(curdir, "zeoservice.py.in")).read()
        zeo_file = os.path.join(self.options["bin-directory"], "%s.py" % zeo_filename)
        self._write_file(zeo_file, zeo_service % arguments)

        zc.buildout.easy_install.scripts(
            [(zeo_filename, zeo_filename, "main")],
            self.zodb_ws,
            self.options["executable"],
            self.options["bin-directory"],
            extra_paths=path,
            relative_paths=self._relative_paths,
            initialization=self.options.get("initialization", ""),
        )

    def _write_file(self, path, content):
        logger = logging.getLogger("zc.buildout.easy_install")
        f = open(path, "w")
        try:
            f.write(content)
        finally:
            f.close()
        logger.debug("Wrote file %s" % path)
        os.chmod(path, 0o755)
        logger.warning("Changed mode for %s to 755" % path)


# the template used to build a regular file storage entry for zeo.conf
file_storage_template = """
<filestorage %(storage_number)s>
  path %(file_storage)s
  %(pack_gc)s
  %(pack_keep_old)s
</filestorage>
""".strip()


# the template used to build a blob storage

blob_storage_template = """
<filestorage %(storage_number)s>
  path %(file_storage)s
  blob-dir %(blob_storage)s
  %(pack_gc)s
  %(pack_keep_old)s
</filestorage>
""".strip()

zrs_template = """
%%import zc.zrs

<zrs %(storage_number)s>
 %(replicate)s
 keep-alive-delay %(keep_alive)s
 %(storage)s
</zrs>""".strip()


z_log_file = """\
    <logfile>
      path %(filename)s
      format %(logformat)s
      %(zeo_log_rotate)s
    </logfile>
""".strip()

authentication_template = """
  authentication-protocol digest
  authentication-database %(database)s
  authentication-realm %(realm)s
"""

# The template used to build zeo.conf
zeo_conf_template = """\
%%define INSTANCE %(instance_home)s

<zeo>
  address %(zeo_address)s
  read-only %(read_only)s
  invalidation-queue-size %(invalidation_queue_size)s
  pid-filename %(pid_file)s
  %(authentication)s
  %(monitor_address)s
</zeo>

%(storage)s

<eventlog>
  level %(zeo_log_level)s
  %(z_log)s
</eventlog>

<runner>
  program $INSTANCE/bin/runzeo
  socket-name %(socket_name)s
  daemon true
  forever false
  backoff-limit 10
  exit-codes 0, 2
  directory $INSTANCE
  default-to-interactive true
  %(effective_user)s

  # This logfile should match the one in the zeo.conf file.
  # It is used by zdctl's logtail command, zdrun/zdctl doesn't write it.
  logfile %(z_log_filename)s
</runner>

%(zeo_conf_additional)s
"""
