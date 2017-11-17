# encoding: utf-8

import threading
from .expect import Base as Expect
from .action import Base as Action

class Trigger(object):
    def __init__(self, expect, action, timeout = 0):
        assert isinstance(expect, Expect)
        assert isinstance(action, Action)
        assert isinstance(timeout, float) and 0 <= timeout
        self.expect = expect
        self.action = action
        self.timeout = timeout

    def fire(self, player, context):
        if not self.expect.test(player, context):
            return False
        thread = threading.Thread(
            target = self.action.invoke,
            args = (player, context)
        )
        thread.daemon = True
        thread.start()
        thread.join(self.timeout or self.action.timeout)
        return True
