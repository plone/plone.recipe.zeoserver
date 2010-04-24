import logging
import socket
import sys

from ZEO.ClientStorage import ClientStorage


def _main(host, port, unix=None, days=1, username=None, password=None,
         realm=None, blob_dir=None, shared_blob_dir=True, storage='1'):
    if unix is not None:
        addr = unix
    else:
        if host is None:
            host = socket.gethostname()
        addr = host, int(port)

    wait = True
    cs = None
    try:
        cs = ClientStorage(
            addr, storage=storage, wait=wait, read_only=True,
            username=username, password=password, realm=realm,
            blob_dir=blob_dir, shared_blob_dir=shared_blob_dir,
        )
        cs.pack(wait=wait, days=int(days))
    finally:
        if cs is not None:
            cs.close()


def main(*args, **kw):
    root_logger = logging.getLogger()
    old_level = root_logger.getEffectiveLevel()
    logging.getLogger().setLevel(logging.WARNING)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(name)s %(levelname)s %(message)s"))
    logging.getLogger().addHandler(handler)
    try:
        _main(*args, **kw)
    finally:
        logging.getLogger().setLevel(old_level)
        logging.getLogger().removeHandler(handler)


if __name__ == "__main__":
    main()
