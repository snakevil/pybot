# encoding: utf-8

import threading
from .. import core
from .expect import Base as Expect
from .react import Base as React
from .react.etimeout import ETimeout

class Reflex(object):
    def __init__(self, expect, react, title = '', timeout = 0):
        if not isinstance(expect, Expect):
            raise core.EType(expect, Expect)
        if not isinstance(react, React):
            raise core.EType(react, React)
        if not isinstance(timeout, float) \
                and not isinstance(timeout, int) \
                or 0 > timeout:
            raise ETimeout(timeout)
        self._title = title or str(expect)
        self._expect = expect
        self._react = react
        self._timeout = timeout

    def __repr__(self):
        return 'Reflex(%r, %r, %r%s)' % (
            self._title,
            self._expect,
            self._react,
            '' if not self._timeout else ', %d' % self._timeout
        )

    def __str__(self):
        return self._title

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
        event.log('%s in %s?' % (event.target, self._expect), 0)
        trace = []
        matched = self._expect.test(event, trace)
        self._tracelog(event, ['%r %r' % (self._expect, matched), trace], '?')
        if not matched:
            return False
        event['title'] = self._title
        event['__spots__'] = self._expect.spots
        event.log('%s %s' % (event.target, self._title), 1)
        trace = []
        thread = threading.Thread(
            target = self._react.do,
            args = (event, trace)
        )
        thread.daemon = True
        thread.start()
        thread.join(self._timeout or self._react.timeout)
        self._tracelog(event, [repr(self._react), trace], '!')
        if thread.is_alive():
            event.log('%s %s timeout' % (event.target, self._title), 3)
        return True

    def _tracelog(self, event, trace, symbol, level = 1):
        prefix = '  ' * level
        for item in trace:
            if isinstance(item, list):
                if item:
                    self._tracelog(event, item, symbol, 1 + level)
            else:
                event.log('%s%s %s' % (prefix, symbol, item), 0)
