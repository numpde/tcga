# RA, 2021-03-17

class Peek:
    def __init__(self, reporter=None):
        self.reporter = reporter

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, x=None):
        if self.reporter is not None:
            self.reporter(x)
        return x
