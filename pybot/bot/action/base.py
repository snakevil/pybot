# encoding: utf-8

class Base(object):
    def __init__(self, timeout = .1):
        assert (
            isinstance(timeout, float) or isinstance(timeout, int)
        ) and 0 < timeout
        self.timeout = timeout

    def do(self, event):
        assert False
