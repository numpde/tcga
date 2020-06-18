# RA, 2020-06-17

"""
Copy of the AAindex database.

https://www.genome.jp/aaindex/
https://en.wikipedia.org/wiki/AAindex
ftp://ftp.genome.jp/pub/db/community/aaindex/
"""

import wget

from pathlib import Path
from datetime import datetime, timezone

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

    'local': ROOT_PATH / "data",
}


def download(url: str):
    assert url

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
        print("Done:", download(url))


if __name__ == '__main__':
    download_all()
