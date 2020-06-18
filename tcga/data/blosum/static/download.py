# RA, 2020-06-15

"""
Download the BLOSUM matrices.
"""

import wget

from pathlib import Path
from datetime import datetime, timezone

ROOT_PATH = Path(__file__).parent

PARAM = {
    'urls': {
        "https://raw.githubusercontent.com/wrpearson/fasta36/7c0dba1dfe5fc92d937f2bd5f9c90b8bfdb14743/data/blosum45.mat",
        "https://raw.githubusercontent.com/wrpearson/fasta36/7c0dba1dfe5fc92d937f2bd5f9c90b8bfdb14743/data/blosum50.mat",
        "https://raw.githubusercontent.com/wrpearson/fasta36/7c0dba1dfe5fc92d937f2bd5f9c90b8bfdb14743/data/blosum62.mat",
        "https://raw.githubusercontent.com/wrpearson/fasta36/7c0dba1dfe5fc92d937f2bd5f9c90b8bfdb14743/data/blosum80.mat",
    },

    'local': ROOT_PATH / "data",
}


def download(url: str):
    out = PARAM['local'] / Path(url).name
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
        print(download(url))


if __name__ == '__main__':
    download_all()
