# encoding: utf-8

from ... import image, player
from .expect import Expect
from .etemplate import ETemplate

class Template(Expect):
    """docstring for Template"""
    def __init__(self, template, region = None, **spots):
        super(Template, self).__init__(**spots)
        self._spots = self.spots.copy()
        try:
            self._needle = image.template(template)
        except:
            raise ETemplate(template)
        self._region = region if not region or isinstance(region, player.Rect) \
            else player.Rect(*region)

    def __repr__(self):
        return 'Template(%r%s)' % (
            self._needle,
            '' if not self._region \
                else ', %r' % self._region
        )

    def test(self, event):
        if not event.screen:
            return False
        x0 = y0 = 0
        zone = event.screen
        if self._region:
            x0 = self._region.left
            y0 = self._region.top
            zone = event.screen.crop(
                (x0, y0),
                (self._region.right, self._region.bottom)
            )
        x, y = self._search(zone.grayscale().binary(self._needle.threshold))
        if 0 > x:
            return False
        x += x0
        y += y0
        self.spots = {
            k: (v[0].skew(x, y), v[1]) for k, v in self._spots.items()
        }
        return True

    def _search(self, haystack):
        candinates = []
        width = haystack.width - self._needle.width + 1
        for y in range(haystack.height - self._needle.height + 1):
            candinates += range(haystack.width * y, haystack.width * y + width)
        size = self._needle.width * 4
        times = 0
        for y in range(self._needle.height):
            filtered = []
            template = self._needle.rgba[size * y:size * (y + 1)]
            for i in candinates:
                j = (i + haystack.width * y) * 4
                times += 1
                if haystack.rgba[j:j + size] == template:
                    filtered.append(i)
            candinates = filtered
            if not len(candinates):
                break
        if not candinates:
            return (-1, -1)
        return (
            candinates[0] % haystack.width,
            candinates[0] // haystack.width
        )
