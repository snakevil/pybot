# encoding: utf-8

import threading
from .expect import Base as Expect
from .action import Base as Action

class Trigger(object):
    def __init__(self, expect, action, timeout = 0):
        assert isinstance(expect, Expect)
        assert isinstance(action, Action)
        assert (
            isinstance(timeout, float) or isinstance(timeout, int)
        ) and 0 <= timeout
        self.expect = expect
        self.action = action
        self.timeout = timeout

    def fire(self, event):
        if not self.expect.test(event):
            return False
        thread = threading.Thread(
            target = self.action.do,
            args = (event,)
        )
        thread.daemon = True
        thread.start()
        thread.join(self.timeout or self.action.timeout)
        return True
