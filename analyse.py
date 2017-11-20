# encoding: utf-8

import sys
import pybot

assert 5 < len(sys.argv)

pic = pybot.image.load(
    sys.argv[1]
).crop(
    (int(sys.argv[2]), int(sys.argv[3])),
    (int(sys.argv[4]), int(sys.argv[5]))
)
print('histogram: %r' % (pic.histogram(1),))

pic = pic.resize(8, 8).grayscale()
print('threshold: %r' % pic.threshold)
print('fingerprint: %r' % pic.binary().digest)
