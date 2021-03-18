# RA, 2020-12-06
# RA, 2021-03-18

import datetime
import inspect


def whatsmyname() -> str:
    return inspect.currentframe().f_back.f_code.co_name


class Now:
    def __init__(self, sep=' '):
        self.sep = sep
        self.t = datetime.datetime.now(tz=datetime.timezone.utc)

    @property
    def utc_iso(self):
        return self.t.isoformat(sep=self.sep, timespec='seconds')

    @property
    def utc_iso_ms(self):
        return self.t.isoformat(sep=self.sep, timespec='microseconds')

    def __str__(self):
        return self.t.strftime("%Z-%Y%m%d-%H%M%S")
