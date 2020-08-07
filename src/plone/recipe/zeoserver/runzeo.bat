@rem %(PACKAGE)s instance start script
@set PYTHON=%(PYTHON)s
@set ZODB_HOME=%(zodb3_home)s
@set CONFIG_FILE=%(INSTANCE_HOME)s/etc/%(PACKAGE)s.conf
@set PYTHONPATH=%(PYTHONPATH)s
@set RUNZEO=%%ZODB_HOME%%/ZEO/runzeo.py
"%%PYTHON%%" "%%RUNZEO%%" -C "%%CONFIG_FILE%%" %%1 %%2 %%3 %%4 %%5 %%6 %%7 %%8 %%9
