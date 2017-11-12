# encoding: utf-8

from ...player import Window

class Base(object):
    def __init__(self):
        self.context = {}

    def __and__(self, another):
        assert False

    def __iand__(self, another):
        return self.__and__(another)

    def __or__(self, another):
        assert False

    def __ior__(self, another):
        return self.__or__(another)

    def log(self, message):
        message = '%s /%s/ %s' % (
            self.player,
            type(self).__name__,
            message
        )
        log = self.context.get('dbg')
        if hasattr(log, '__call__'):
            log(message)

    def test(self, player, context = {}):
        assert isinstance(player, Window)
        self.player = player
        assert isinstance(context, dict)
        self.context = context
        return False
