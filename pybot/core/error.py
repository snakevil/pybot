# encoding: utf-8

class Error(Exception):
    def __init__(self, code, reason):
        super(Error, self).__init__()
        self.code = code
        self.reason = reason

    def __str__(self):
        return self.reason
