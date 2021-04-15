# RA, 2020-12-06
# RA, 2021-03-18

import datetime
import inspect
import contextlib


def whatsmyname() -> str:
    return inspect.currentframe().f_back.f_code.co_name


# https://stackoverflow.com/questions/34491808/how-to-get-the-current-scripts-code-in-python
# https://docs.python.org/3/library/inspect.html
def this_module_body(goback=1):
    return inspect.getsource(inspect.getmodule(inspect.stack()[goback].frame))


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


@contextlib.contextmanager
def Section(description="", printer=None):
    from time import time as tic
    fname = inspect.currentframe().f_back.f_back.f_code.co_name
    printer and printer(f"{fname} -- {description}...")
    start = tic()
    yield
    printer and printer(f"{fname} -- {description} [{(tic() - start):.2g}s].")
