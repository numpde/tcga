# RA, 2020-06-18

import datetime


class Annotations:
    def __init__(self):
        self.d = {}
        self[self] = {
            'timestamp': datetime.datetime.now(tz=datetime.timezone.utc).isoformat(sep=' '),
        }

    def __setitem__(self, obj, value: dict):
        if type(value) is not dict:
            raise ValueError(F"'References' only accepts a value of type dict, got '{type(value)}'.")
        if id(obj) in self.d:
            raise KeyError(F"The key '{id(obj)}' of object already exists (obj: {obj}).")
        self.d[id(obj)] = dict(value)

    def __getitem__(self, obj):
        if obj not in self:
            self[obj] = dict()

        return self.d[id(obj)]

    def __contains__(self, obj):
        return (id(obj) in self.d)

    # def __call__(self, value: dict, obj):
    #     self[obj] = value
    #     return obj


annotations = Annotations()
