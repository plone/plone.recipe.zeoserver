@rem %(PACKAGE)s instance start script
@set PYTHON=%(PYTHON)s
@set ZODB_HOME=%(zodb_home)s
@set CONFIG_FILE=%(INSTANCE_HOME)s/etc/%(PACKAGE)s.conf
@set PYTHONPATH=%(PYTHONPATH)s
@set RUNZEO=ZEO.runzeo
"%%PYTHON%%" -m "%%RUNZEO%%" -C "%%CONFIG_FILE%%" %%1 %%2 %%3 %%4 %%5 %%6 %%7 %%8 %%9
