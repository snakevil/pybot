# encoding: utf-8

import platform
system = platform.system()
if 'Windows' == system:
    from ._decorate import _win32 as _decorate
elif 'Darwin' == system:
    from ._decorate import _macos as _decorate
else:
    from ._decorate import _linux as _decorate
import time
from ..image import Screenshot
from ._struct import Rect

get_euid = _decorate.get_euid
su = _decorate.su

class Window(object):
    def __init__(self, handle):
        self._handle = handle
        self.pid = _decorate.get_pid(handle)
        self.title = '.%d' % self.pid

    def __str__(self):
        return self.title

    @classmethod
    def first(cls, pattern):
        handles = _decorate.query(pattern)
        if 0 < len(handles):
            return cls(handles[0])

    @classmethod
    def all(cls, pattern):
        return [cls(handle) for handle in _decorate.query(pattern)]

    def aka(self, nickname):
        self.title = '@' + nickname if nickname \
            else '.%d' % self.pid
        return self

    def idle(self, msecs):
        time.sleep(msecs / 1000)
        return self

    @property
    def minimized(self):
        return _decorate.is_minimized(self._handle)

    def minimize(self):
        if self.minimized:
            return self
        _decorate.minimize(self._handle)
        return self.idle(10)

    def restore(self):
        if not self.minimized:
            return self
        _decorate.restore(self._handle)
        return self.idle(10)

    def focus(self):
        self.restore()
        _decorate.foreground(self._handle)
        return self

    @property
    def window(self):
        return Rect(*_decorate.get_rect(self._handle))

    @property
    def width(self):
        return _decorate.get_size(self._handle)[0]

    @property
    def height(self):
        return _decorate.get_size(self._handle)[1]

    def click(self, point):
        _decorate.click(self._handle, point.x, point.y)
        return self.idle(90)

    def drag(self, start, end):
        _decorate.drag(self._handle, (start.x, start.y), (end.x, end.y))
        return self.idle(90)

    def snap(self):
        if not self.width or not self.height:
            return
        return Screenshot(
            _decorate.get_size(self._handle),
            _decorate.grab(self._handle)
        )
