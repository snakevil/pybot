# encoding: utf-8

import threading
from .. import core
from .expect import Base as Expect
from .react import Base as React
from .react.etimeout import ETimeout

class Reflex(object):
    def __init__(self, expect, react, timeout = 0, title = ''):
        if not isinstance(expect, Expect):
            raise core.EType(expect, Expect)
        if not isinstance(react, React):
            raise core.EType(react, React)
        if not isinstance(timeout, float) \
                and not isinstance(timeout, int) \
                or 0 > timeout:
            raise ETimeout(timeout)
        self._expect = expect
        self._react = react
        self._timeout = timeout
        self._title = title

    def __repr__(self):
        return 'Reflex(%r, %r%s)' % (
            self._expect,
            self._react,
            '' if not self._timeout else ', %d' % self._timeout
        )

    def __str__(self):
        return self._title or type(self).__name__

    def __iadd__(self, other):
        if isinstance(other, React):
            self._react += other
        elif isinstance(other, Reflex) and self._expect == other._expect:
            self._react += other._react
        else:
            raise core.EType(other, React)
        return self

    @property
    def expect(self):
        return self._expect

    def then(self, react):
        self += react
        return self

    def do(self, event):
        if not self._expect.test(event):
            return False
        event['__spots__'] = self._expect.spots
        event.log('%s %s' % (event.target, self._expect), 1)
        thread = threading.Thread(
            target = self._react.do,
            args = (event,)
        )
        thread.daemon = True
        thread.start()
        thread.join(self._timeout or self._react.timeout)
        if thread.is_alive():
            event.log('%s %s timeout' % (event.target, self._expect), 3)
        return True
