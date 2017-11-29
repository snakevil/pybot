# encoding: utf-8

from .error import Error

class ETodo(Error):
    def __init__(self, feature = None):
        reason = 'Feature unimplemented.'
        if feature:
            reason = "Feature '%s' unimplemented." % feature
        super(ETodo, self).__init__(1, reason, feature = feature)
