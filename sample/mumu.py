# encoding: utf-8

from pybot.player import Window, Point

class MuMu(Window):
    __pattern = '阴阳师 - MuMu模拟器$'

    @classmethod
    def first(cls):
        return super(MuMu, cls).first(cls.__pattern)

    @classmethod
    def all(cls):
        return super(MuMu, cls).all(cls.__pattern)

    @property
    def width(self):
        width = super(MuMu, self).width
        return width - 2 if width else 0

    @property
    def height(self):
        return (self.width >> 4) * 9

    def click(self, point):
        return super(MuMu, self).click(
            Point(point.x + 1, point.y + 35)
        )

    def drag(self, start, end):
        return super(MuMu, self).drag(
            Point(start.x + 1, start.y + 35),
            Point(end.x + 1, end.y + 35)
        )

    def snap(self):
        snap = super(MuMu, self).snap()
        return None if not snap \
            else snap.crop((1, 35), (self.width + 1, self.height + 35))
