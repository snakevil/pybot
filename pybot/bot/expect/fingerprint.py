# encoding: utf-8

from ... import player
from .expect import Expect
from .efingerprint import EFingerprint
from .egray import EGray
from .ethreshold import EThreshold

class Fingerprint(Expect):
    def __init__(self, region, digest, gray, threshold = 10, **spots):
        if not isinstance(digest, str) or 16 != len(digest):
            raise EFingerprint(digest)
        if not isinstance(gray, int) or 1 > gray or gray > 254:
            raise EGray(gray)
        if not isinstance(threshold, int) or 0 > threshold:
            raise EThreshold(threshold)
        super(Fingerprint, self).__init__(**spots)
        self._region = region if isinstance(region, player.Rect) \
            else player.Rect(*region)
        self._digest = digest
        self._threshold = threshold
        self._gray = gray

    def __repr__(self):
        return 'Fingerprint(%r, %r, %d%s)' % (
            self._region,
            self._digest,
            self._gray,
            '' if 10 == self._threshold \
                else ', %d' % self._threshold
        )

    def _test(self, event, trace):
        digest = event.screen.crop(
            (self._region.left, self._region.top),
            (self._region.right, self._region.bottom)
        ).resize(
            8, 8
        ).grayscale().binary(
            self._gray
        ).digest
        distance = self._measure(self._digest, digest)
        trace.append('= %8.3f/%8.3f %r' % (distance, self._threshold, digest))
        return distance <= self._threshold

    def _measure(self, a, b):
        a_len = len(a)
        b_len = len(b)
        distance = 4 * abs(a_len - b_len)
        for i in range(min(a_len, b_len)):
            if a[i] != b[i]:
                a_bin = bin(int(a[i], 16))[2:].zfill(4)
                b_bin = bin(int(b[i], 16))[2:].zfill(4)
                for j in range(4):
                    if a_bin[j] != b_bin[j]:
                        distance += 1
        return 25 * distance / max(a_len, b_len)
