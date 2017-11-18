# encoding: utf-8

import threading
from .expect import Base as Expect
from .action import Base as Action

class Trigger(object):
    def __init__(self, expect, action, timeout = 0, title = ''):
        assert isinstance(expect, Expect)
        assert isinstance(action, Action)
        assert (
            isinstance(timeout, float) or isinstance(timeout, int)
        ) and 0 <= timeout
        self._expect = expect
        self._action = action
        self._timeout = timeout
        self._title = title or str(expect)

    def fire(self, event):
        if not self._expect.test(event):
            return False
        event.log('&%s triggered' % self._title, 0)
        thread = threading.Thread(
            target = self._action.do,
            args = (event,)
        )
        thread.daemon = True
        thread.start()
        thread.join(self._timeout or self._action.timeout)
        if thread.is_alive():
            event.log('&%s timeout' % self._timeout, 2)
        return True
