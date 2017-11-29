# encoding: utf-8

from .error import Error

class EType(Error):
    def __init__(self, obj, type):
        super(EType, self).__init__(
            2,
            'Illegal %s %r.' % (type.__name__, obj),
            type = type,
            object = obj
        )
