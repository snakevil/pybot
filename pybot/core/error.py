# encoding: utf-8

class Error(Exception):
    def __init__(self, code, reason, **context):
        super(Error, self).__init__()
        self.code = code
        self.reason = reason
        self.context = context

    def __str__(self):
        return self.reason
