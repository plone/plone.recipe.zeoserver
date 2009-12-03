# zeopack wrapper

import socket
from ZEO.ClientStorage import ClientStorage

HAS_BLOB = True
try:
    from ZODB.interfaces import IBlobStorage; IBlobStorage
except ImportError:
    HAS_BLOB = False


def main(host, port, unix=None, days=1, username=None, password=None,
         realm=None, blob_dir=None, storage='1'):
    if unix is not None:
        addr = unix
    else:
        if host is None:
            host = socket.gethostname()
        addr = host, int(port)

    wait = True
    cs = None
    try:
        if HAS_BLOB:
            cs = ClientStorage(
                addr, storage=storage, wait=wait, read_only=True,
                username=username, password=password, realm=realm,
                blob_dir=blob_dir
            )
        else:
            cs = ClientStorage(
                addr, storage=storage, wait=wait, read_only=True,
                username=username, password=password, realm=realm
            )
        cs.pack(wait=wait, days=int(days))
    finally:
        if cs is not None:
            cs.close()


if __name__ == "__main__":
    main()
