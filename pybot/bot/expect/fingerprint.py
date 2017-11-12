# encoding: utf-8

from ...player import Rect
from .expect import Expect

class Fingerprint(Expect):
    def __init__(self, region, otsu, gray = 0, threshold = 10):
        assert isinstance(otsu, str)
        assert isinstance(gray, int) and 0 <= gray and gray < 255
        assert isinstance(threshold, int) and 0 <= threshold
        super(Fingerprint, self).__init__()
        self.region = region if isinstance(region, Rect) \
            else Rect(*region)
        self.otsu = otsu
        self.threshold = threshold
        self.gray = gray

    def test(self, player, context = {}):
        super(Fingerprint, self).test(player, context)
        image = player.snap()
        if not image:
            return False
        otsu = image.crop(
            (self.region.left, self.region.top),
            (self.region.right, self.region.bottom)
        ).resize(8, 8).grayscale().otsu(self.gray)
        distance = self._measure(self.otsu, otsu)
        if distance > self.threshold:
            self.log('%s in D%.2f {%s}' % (self.region, distance, otsu))
            return False
        return True

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
