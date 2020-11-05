# RA, 2020-06-24


import io
import pandas
import hashlib
import base64
import json
import contextlib
import pathlib
import zipfile
import typing
import datetime
import inspect
import copy
import tcga.refs

import shutil
import urllib.request


class _:
    downloads = []

    class Download:
        def __init__(self, **kwargs):
            self._ = pandas.Series({
                'meta': {}, 'url': None, 'local_folder': None, 'again': False,
                **(kwargs or {}),
            })

        @property
        def local_folder(self) -> pathlib.Path:
            return self._.local_folder

        def to(self, *, rel_path=None, abs_path=None):
            if (bool(abs_path) == bool(rel_path)):
                raise RuntimeError("Either rel_path /or/ abs_path must be specified.")
            if abs_path:
                local_folder = pathlib.Path(abs_path)
            else:
                f = inspect.currentframe().f_back
                local_folder = (pathlib.Path(f.f_code.co_filename).parent / rel_path)
            return type(self)(**{**self._, 'local_folder': local_folder})

        def __call__(self, url: str):
            return type(self)(**{**self._, 'url': url})

        def again(self, again=False):
            return type(self)(**{**self._, 'again': again})

        def with_meta(self, meta: dict):
            assert 'source' not in meta
            assert 'datetime' not in meta
            assert json.loads(json.dumps(meta)) == meta, "The specified metadata should be json-stable."
            return type(self)(**{**self._, 'meta': meta})

        @property
        def now(self):
            if not self._.url:
                raise RuntimeError("What do you want to download?")
            if not self._.local_folder:
                raise RuntimeError("Use  .to(...)  to set the local folder before downloading.")

            name = base64.urlsafe_b64encode(hashlib.sha256(self._.url.encode()).digest()).decode()
            local_file = (pathlib.Path(self._.local_folder) / name).with_suffix(".zip")

            if self._.again or not local_file.exists():
                local_file.parent.mkdir(exist_ok=True, parents=True)

                assert 'url' not in self._.meta
                assert 'datetime' not in self._.meta

                with contextlib.closing(urllib.request.urlopen(url=self._.url)) as rd:
                    with zipfile.ZipFile(local_file, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                        with zf.open("data", mode='w', force_zip64=True) as fd:
                            shutil.copyfileobj(rd, fd)
                        with zf.open("meta", mode='w') as fd:
                            meta = self._.meta.copy()
                            meta['source'] = self._.url
                            meta['datetime'] = datetime.datetime.now(tz=datetime.timezone.utc).isoformat(sep=' ')
                            fd.write(json.dumps(meta).encode())

            assert local_file.exists()

            with zipfile.ZipFile(local_file, mode='r') as zf:
                with zf.open("meta") as fd:
                    meta = json.loads(fd.read().decode())
                    for (k, v) in self._.meta.items():
                        if k not in meta:
                            raise RuntimeWarning("The specified metadata is not in the file. Use again(True).")
                        if not (meta[k] == v):
                            raise RuntimeWarning(
                                "The specified metadata differs from the file. Use again(True).")
                    meta = {**self._.meta, **meta}

            class Local:
                def __init__(self, local_file: pathlib.Path, meta: dict):
                    self.local_file = local_file
                    self.meta = meta

                def __call__(self):
                    return self

                @contextlib.contextmanager
                def open(self, mode='r'):
                    assert mode in ["r", "rb"]
                    with zipfile.ZipFile(self.local_file, mode='r') as _:
                        with _.open("data") as _:
                            if mode == "rb":
                                yield _
                            else:
                                yield io.TextIOWrapper(_)

                @property
                def bytes(self) -> bytes:
                    with self.open(mode='rb') as _:
                        return _.read()

                @property
                def text(self) -> str:
                    with self.open(mode='r') as _:
                        return _.read()

                @property
                def json(self):
                    return json.loads(self.text)

            obj = Local(local_file, meta)

            try:
                # Keep reference to avoid id(...) clash
                _.downloads.append(obj)

                tcga.refs.annotations[obj] = meta
            except KeyError:
                raise RuntimeWarning(F"This error may happen if you download several file but discard the .now object.")

            return obj


download = _.Download()
