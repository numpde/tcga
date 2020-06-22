# RA, 2020-06-17

"""
Copy of the AAindex database.

https://www.genome.jp/aaindex/
https://en.wikipedia.org/wiki/AAindex
ftp://ftp.genome.jp/pub/db/community/aaindex/
"""

import re

import wget
import time
import pickle
import zipfile
import numpy as np
import pandas as pd

from tcga.utils import First

from typing import Iterable
from pathlib import Path
from datetime import datetime, timezone
from itertools import groupby, chain
from collections import OrderedDict
from more_itertools import first

ROOT_PATH = Path(__file__).parent

PARAM = {
    'urls': {
        "ftp://ftp.genome.jp/pub/db/community/aaindex/aaindex.doc",
        "ftp://ftp.genome.jp/pub/db/community/aaindex/aaindex1",
        "ftp://ftp.genome.jp/pub/db/community/aaindex/aaindex2",
        "ftp://ftp.genome.jp/pub/db/community/aaindex/aaindex3",
        "https://www.genome.jp/aaindex/AAindex/list_of_indices",
        "https://www.genome.jp/aaindex/AAindex/list_of_matrices",
        "https://www.genome.jp/aaindex/AAindex/list_of_potentials",
    },

    'original': ROOT_PATH / "original",
    'parsed': ROOT_PATH / "parsed/aaindex.pkl.zip",
}


def download(url: str):
    assert url

    out = PARAM['original'] / Path(url).name
    out.parent.mkdir(exist_ok=True, parents=True)

    if out.exists():
        return out

    wget.download(str(url).format(), str(out))

    with open(str(out) + "_meta.txt", 'w') as fd:
        print("Downloaded on {} from".format(datetime.now(tz=timezone.utc)), file=fd)
        print(url, file=fd)

    return out


def download_all():
    for url in PARAM['urls']:
        yield download(url)


def parse_list_file(file: Path) -> pd.Series:
    with file.open('r') as fd:
        df = pd.DataFrame(re.findall(r"\n([0-9A-Z]+)\s+(.*)\n", ('\n' + fd.read())), columns=["AAindex", "Description"])
        return df.set_index("AAindex").Description


def parse(k, g):
    g = [re.sub(r"\s+", ' ', c[2:]).strip() for c in g]
    if (k in "HDRATJ*"):
        return ' '.join(g)
    if (k == "I"):
        assert (len(g) == 3)
        cols = chain.from_iterable(zip(*re.findall(r"([A-Z])/([A-Z])[ ]*", g[0])))
        data = chain.from_iterable([c.split() for c in g[1:]])
        return pd.to_numeric(pd.Series(index=cols, data=data), errors='coerce')
    if (k == "C"):
        data = list(chain.from_iterable(re.findall(r"([\w]+)\s+([-+.\w]+)", c) for c in g))
        return pd.to_numeric(pd.DataFrame(data, columns=['id', 'v']).set_index('id').v, errors='coerce')
    if (k == "M"):
        p = g[0]
        p = re.fullmatch(r"(.*)(rows)([=\s]+)(?P<rows>[-\w]+)(.*)(cols)([=\s]+)(?P<cols>[-\w]+)(.*)", p).groupdict()
        data = [c.split() for c in g[1:]]
        assert len(p['rows']) == len(data)
        assert len(p['cols']) == max(map(len, data))
        df = pd.DataFrame(data=data, index=list(p['rows']), columns=list(p['cols']))
        df = df.apply(pd.to_numeric, errors='coerce')
        if df.where(np.triu(np.ones_like(df, dtype=bool), 1)).isna().all().all():
            # The upper triangle is all-nan; symmetrize
            df = df.where(~df.isna(), df.T)
        return df
    raise NotImplementedError


def parse_aaindex_file(file: Path) -> Iterable[pd.Series]:
    class ffill:
        def __init__(self, na):
            self.na = na
            self.last = na

        def __call__(self, x):
            if (x == self.na):
                return self.last
            else:
                self.last = x
                return x

    def fix(s):
        # Bugs in entry DOSZ010101--DOSZ010104
        s = s.replace("cols rows =", "cols =")
        s = s.replace("Doszt?yi", "Dosztanyi")
        return s

    def records(s):
        return filter(lambda r: len(r), map(str.strip, s.split(sep="\n//")))

    with file.open('r') as fd:
        for rec in records(fix(fd.read())):
            try:
                yield pd.Series(OrderedDict([
                    (k, parse(k, list(g)))
                    for (k, g) in groupby(rec.split('\n'), key=First(first).then(ffill(' ')))
                ]))
            except Exception as ex:
                print("Failed on:")
                print(rec.strip())
                print(F"because of: {ex}")
                time.sleep(1)
                raise


def main():
    files = sorted(download_all())

    data = {
        'aaindex': pd.DataFrame(OrderedDict(
            (rec['H'], rec)
            for file in files
            if re.match(r"(.*/aaindex[0-9])$", str(file))
            for rec in parse_aaindex_file(file)
        )),
        **{
            file.stem: parse_list_file(file)
            for file in files
            if re.match(r"(.*/list_.*)$", str(file))
        }
    }

    for k in data.keys():
        if k.startswith("list"):
            for i in data[k].index:
                assert i in data['aaindex']

    # SAVE TO DISK

    out = PARAM['parsed']
    out.parent.mkdir(exist_ok=True, parents=True)

    with zipfile.ZipFile(out, mode='w', compression=zipfile.ZIP_LZMA) as zf:
        with zf.open(str(out.with_suffix(".pkl").name), mode='w') as fd:
            pickle.dump(data, fd)

    meta = '\n'.join(
        str(file.name) + ": \n" + open(str(file) + "_meta.txt", 'r').read()
        for file in files
    )

    out_meta = Path(str(out) + "_meta.txt")
    with out_meta.open('w') as fd:
        print("Created on {} using".format(datetime.now(tz=timezone.utc)), file=fd)
        print("", file=fd)
        print(meta, file=fd)

    print(F"Done; see {out_meta}")


if __name__ == '__main__':
    main()
