# encoding: utf-8

import time
from ... import image, player
from .expect import Expect
from .etemplate import ETemplate
from .ethreshold import EThreshold

class Template(Expect):
    """docstring for Template"""
    def __init__(self, template, region = None, threshold = 10, **spots):
        super(Template, self).__init__(**spots)
        self._spots = self.spots.copy()
        self._template = template
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
        return 'Template(%r%s%s)' % (
            self._template,
            '' if not self._region \
                else ', %r' % self._region,
            '' if 10 == self._threshold \
                else ', %d' % self._threshold
        )

    def _test(self, event, trace):
        x = y = 0
        zone = event.screen
        if self._region:
            x = self._region.left
            y = self._region.top
            zone = event.screen.crop(
                (x, y),
                (self._region.right, self._region.bottom)
            )
        t0 = time.time()
        matched = self._search(zone.grayscale().binary(self._needle.threshold))
        if not matched:
            return False
        trace.append(
            '%d matches in %.3f ms' % (
                len(matched),
                1000 * (time.time() - t0)
            )
        )
        for point, distance in matched:
            trace.append(
                '= %8.3f/%8.3f (%d, %d)' % (
                    distance,
                    self._threshold,
                    point[0] + x,
                    point[1] + y
                )
            )
        x += matched[0][0][0]
        y += matched[0][0][1]
        self.spots = {
            k: (v[0].skew(x, y), v[1]) for k, v in self._spots.items()
        }
        return True

    def _search(self, haystack):
        width = haystack.width - self._needle.width + 1
        candidates = [
            (i, 0) \
                for y in range(haystack.height - self._needle.height + 1) \
                for i in range(haystack.width * y, haystack.width * y + width)
        ]
        width = self._needle.width << 2
        quota = self._threshold * self._needle.width / 100
        limit = 0
        for y in range(self._needle.height -1, -1, -1):
            limit += quota * y * 2 / (self._needle.height - 1)
            filtered = []
            nline = self._needle.rgba[width * y:width * (y + 1):4]
            for candidate, bad in candidates:
                offset = (candidate + haystack.width * y) << 2
                hline = haystack.rgba[offset:offset + width:4]
                if hline != nline:
                    bad += sum([1 for i, j in zip(hline, nline) if i != j])
                    if bad > limit:
                        continue
                filtered.append((candidate, bad))
            if not filtered:
                return tuple()
            candidates = filtered
        size = self._needle.width * self._needle.height / 100
        return tuple(
            sorted(
                [
                    (
                        (i % haystack.width, i // haystack.width),
                        j / size
                    ) for i, j in candidates
                ],
                key = lambda i: i[1]
            )
        )
