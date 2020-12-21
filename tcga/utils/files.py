# RA, 2020-10-09
# RA, 2020-12-06
# RA, 2020-10-19


import io
import os
import pathlib
import typing
import contextlib


def relpath(path):
    return os.path.relpath(str(path), os.getcwd())


def assert_exists(file):
    if not pathlib.Path(file).exists():
        raise FileNotFoundError(F"Oh, file `{file}`, where art thou?!")
    else:
        return file


@contextlib.contextmanager
def seek_then_rewind(fd: io.IOBase, seek=None) -> io.IOBase:
    pos = fd.tell()
    if seek is not None:
        fd.seek(seek)
    try:
        yield fd
    finally:
        fd.seek(pos)


# Adapted from
# https://stackoverflow.com/a/4213255
def md5(fd: io.TextIOBase) -> str:
    import hashlib
    with seek_then_rewind(fd):
        md5 = hashlib.md5()
        for chunk in iter(lambda: fd.read(128 * md5.block_size).encode(), b''):
            md5.update(chunk)
    return md5.hexdigest()


def mkdir(path: pathlib.Path, parents=True, exists_ok=True):
    assert not path.is_file(), F"Cannot create folder (it is a file: {path})."
    path.mkdir(parents=parents, exist_ok=exists_ok)
    return path
