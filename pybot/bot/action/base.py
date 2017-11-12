# encoding: utf-8

from ...player import Window

class Base(object):
    def __init__(self):
        self.context = {}

    def log(self, message):
        message = '%s <%s> %s' % (
            self.player,
            type(self).__name__,
            message
        )
        log = self.context.get('log')
        if hasattr(log, '__call__'):
            log(message)

    def apply(self, player, context = {}):
        assert isinstance(player, Window)
        assert isinstance(context, dict)
        self.player = player
        self.context = context
        return context
