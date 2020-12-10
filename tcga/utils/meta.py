# RA, 2020-12-06


def whatsmyname() -> str:
    import inspect
    return inspect.currentframe().f_back.f_code.co_name
