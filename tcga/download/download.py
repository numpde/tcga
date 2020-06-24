# RA, 2020-06-24


import io
import base64
import json
import contextlib
import pathlib
import zipfile
import typing
import datetime

import shutil
import urllib.request


class Download:
    default_folder = pathlib.Path(pathlib.Path.cwd() / "download_cache")

    def __init__(self, url: str, zipped=True):
        if not zip:
            raise NotImplementedError("Only zipped=True is implemented.")
        self.meta = {'source': url}

    def with_meta(self, meta: dict):
        assert 'source' not in meta
        assert 'datetime' not in meta
        assert json.loads(json.dumps(meta)) == meta, "The specified metadata is not json-stable."
        self.meta = {**self.meta, **meta}
        return self

    def to(self, local_folder):
        url = self.meta['source']
        assert url
        name = base64.urlsafe_b64encode(url.encode()).decode()
        local_file = (pathlib.Path(local_folder) / name).with_suffix(".zip")

        if not local_file.exists():
            local_file.parent.mkdir(exist_ok=True, parents=True)

            with contextlib.closing(urllib.request.urlopen(url=url)) as rd:
                with zipfile.ZipFile(local_file, mode='w') as zf:
                    with zf.open("data", mode='w') as fd:
                        shutil.copyfileobj(rd, fd)
                    with zf.open("meta", mode='w') as fd:
                        assert 'datetime' not in self.meta
                        self.meta['datetime'] = datetime.datetime.now(tz=datetime.timezone.utc).isoformat(sep=' ')
                        fd.write(json.dumps(self.meta).encode())

        assert local_file.exists()

        with zipfile.ZipFile(local_file, mode='r') as zf:
            with zf.open("meta") as fd:
                meta = json.loads(fd.read().decode())
                for (k, v) in self.meta.items():
                    if k in meta:
                        assert meta[k] == v, "The specified metadata differs from what is in the file."
                meta = {**self.meta, **meta}

        class Local:
            def __init__(self, local_file: pathlib.Path, meta: dict):
                self.local_file = local_file
                self.meta = meta

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


if __name__ == '__main__':
    def example1():
        url = "https://www.ebi.ac.uk/ena/browser/api/fasta/J02459.1"
        x = Download(url).to(Download.default_folder)

        print("[Meta]")
        print(x.meta)

        print("[Bio.Seq]")
        import Bio.SeqIO
        import Bio.Seq
        with x.open('r') as fd:
            print(Bio.SeqIO.read(fd, format='fasta'))


    def example2():
        url = "ftp://ftp.genome.jp/pub/db/community/aaindex/aaindex.doc"
        x = Download(url).with_meta({'xyz': 3}).to(Download.default_folder)
        print(x.meta)
        print(x.text[0:100], "...")


    example2()
    example1()
