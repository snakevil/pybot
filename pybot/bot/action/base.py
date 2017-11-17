# encoding: utf-8

class Base(object):
    def __init__(self, timeout = .1):
        assert isinstance(timeout, float) and 0 < timeout
        self.timeout = timeout

    def invoke(self, player, context):
        assert False
