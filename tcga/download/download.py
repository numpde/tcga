# RA, 2020-06-24


import io
import pandas
import base64
import json
import contextlib
import pathlib
import zipfile
import typing
import datetime
import inspect

import shutil
import urllib.request


class _:
    # class __Download__(type):
    #     def __init__(cls, *args, **kwargs):
    #         cls._last_used_folder = None
    #         super().__init__(*args, **kwargs)
    #
    #     @property
    #     def last_used_folder(cls):
    #         return cls._last_used_folder
    #
    #     @last_used_folder.setter
    #     def last_used_folder(cls, value):
    #         cls._last_used_folder = value

    class Download:
        def __init__(self, **kwargs):
            self._ = pandas.Series({
                'meta': {}, 'url': None, 'local_folder': None, 'renew': False,
                **(kwargs or {}),
            })

        def to(self, *, rel_path=None, abs_path=None):
            if abs_path:
                assert not rel_path
                local_folder = pathlib.Path(abs_path)
            else:
                assert not abs_path
                f = inspect.currentframe().f_back
                local_folder = (pathlib.Path(f.f_code.co_filename).parent / rel_path)
            self._.local_folder = local_folder
            return self

        def __call__(self, url: str):
            return type(self)(**{**self._, 'url': url})

        def renew(self, renew=False):
            return type(self)(**{**self._, 'renew': renew})

        @property
        def local_folder(self) -> pathlib.Path:
            return self._.local_folder

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
                raise RuntimeError("Use .to(...) to set the local folder before downloading.")

            name = base64.urlsafe_b64encode(self._.url.encode()).decode()
            local_file = (pathlib.Path(self._.local_folder) / name).with_suffix(".zip")

            if self._.renew or not local_file.exists():
                local_file.parent.mkdir(exist_ok=True, parents=True)

                with contextlib.closing(urllib.request.urlopen(url=self._.url)) as rd:
                    with zipfile.ZipFile(local_file, mode='w') as zf:
                        with zf.open("data", mode='w') as fd:
                            shutil.copyfileobj(rd, fd)
                        with zf.open("meta", mode='w') as fd:
                            assert 'url' not in self._.meta
                            assert 'datetime' not in self._.meta
                            self._.meta['source'] = self._.url
                            self._.meta['datetime'] = datetime.datetime.now(tz=datetime.timezone.utc).isoformat(sep=' ')
                            fd.write(json.dumps(self._.meta).encode())

            assert local_file.exists()

            with zipfile.ZipFile(local_file, mode='r') as zf:
                with zf.open("meta") as fd:
                    meta = json.loads(fd.read().decode())
                    for (k, v) in self._.meta.items():
                        if k not in meta:
                            raise RuntimeWarning("The specified metadata is not in the file. Use renew(True).")
                        if not (meta[k] == v):
                            raise RuntimeWarning(
                                "The specified metadata differs from the file. Use renew(True).")
                    meta = {**self._.meta, **meta}

            class Local:
                def __init__(self, local_file: pathlib.Path, meta: dict):
                    self.local_file = local_file
                    self.meta = meta

                def __call__(self):
                    return self

                @contextlib.contextmanager
                def open(self, mode='rb'):
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

            return Local(local_file, meta)


download = _.Download()

if __name__ == '__main__':
    def example1():
        url = "https://www.ebi.ac.uk/ena/browser/api/fasta/J02459.1"
        x = download(url).now
        print("[Meta]")
        print(x.meta)

        print("[Bio.Seq]")
        import Bio.SeqIO
        import Bio.Seq
        with x.open('r') as fd:
            print(Bio.SeqIO.read(fd, format='fasta'))


    def example2():
        url = "ftp://ftp.genome.jp/pub/db/community/aaindex/aaindex.doc"
        # download(url).now
        download.to(rel_path="download_cache")
        x = download(url).with_meta({'remember': "Nov 5th"}).now
        # x = download(url).with_meta({'remember': "Dec 5th"}).renew(True).now
        print("Last used:", download.local_folder)
        y = download(url).now
        print(y.meta)

    # from tcga import rootpath

    example2()
    example1()
