# encoding: utf-8

from ... import image, player
from .expect import Expect
from .etemplate import ETemplate
from .ethreshold import EThreshold

class Template(Expect):
    """docstring for Template"""
    def __init__(self, template, region = None, threshold = 10, **spots):
        super(Template, self).__init__(**spots)
        self._spots = self.spots.copy()
        try:
            self._needle = image.template(template)
        except Exception as e:
            raise ETemplate(template)
        self._region = region if not region or isinstance(region, player.Rect) \
            else player.Rect(*region)
        if not isinstance(threshold, int) or 0 > threshold:
            raise EThreshold(threshold)
        self._threshold = threshold

    def __repr__(self):
        return 'Template(%r%s)' % (
            self._needle,
            '' if not self._region \
                else ', %r' % self._region
        )

    def _test(self, event, trace):
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
        trace.append('= %r' % ((x, y),))
        self.spots = {
            k: (v[0].skew(x, y), v[1]) for k, v in self._spots.items()
        }
        return True

    def _search(self, haystack):
        candidates = []
        width = haystack.width - self._needle.width + 1
        for y in range(haystack.height - self._needle.height + 1):
            candidates += [
                (i, 0) for i \
                    in range(haystack.width * y, haystack.width * y + width)
            ]
        threshold = self._threshold * self._needle.width // 100
        width = self._needle.width << 2
        limit = 0
        for y in range(self._needle.height):
            limit += threshold
            filtered = []
            template = self._needle.rgba[width * y:width * (y + 1)]
            for candidate, bad in candidates:
                offset = (candidate + haystack.width * y) << 2
                case = haystack.rgba[offset:offset + width]
                if case == template:
                    filtered.append((candidate, bad))
                else:
                    for i in range(0, width, 4):
                        if case[i] != template[i]:
                            bad += 1
                        if bad > limit:
                            break
                    else:
                        filtered.append((candidate, bad))
            candidates = filtered
            if not len(candidates):
                break
        if not candidates:
            return (-1, -1)
        return (
            candidates[0][0] % haystack.width,
            candidates[0][0] // haystack.width
        )
