#!/usr/bin/env python3
# encoding: utf-8

import sys
from pybot import image

assert 5 < len(sys.argv)

threshold = 0 if 7 > len(sys.argv) else int(sys.argv[6])

region = (
    (int(sys.argv[2]), int(sys.argv[3])),
    (int(sys.argv[4]), int(sys.argv[5]))
)
print('region: %r' % (region,))

pic0 = image.load(
    sys.argv[1]
).crop(*region)
pic0.save('analyse-1-crop.png')
print('histogram: %r' % (pic0.histogram(1),))
pic = pic0.resize(8, 8).grayscale()
print('fingerprint:')
print('  digest: %r' % pic.binary(threshold).digest)
print('  gray: %r' % pic.threshold)

pic = pic0.grayscale()
pic.save('analyse-2-grayscale.png')
print('grayscale:')
print(
    "  map: '''\n%s       '''" % (
        '%s\n' % ('%02x' * pic.width) * pic.height % tuple(pic.rgba[0::4])
    )
)
print(
    "  template: '''\n%s\n            '''" % pic.dump()
)

pic = pic.binary()
pic.save('analyse-2-binary.png')
print('binary:')
print(
    "  map: '''\n%s       '''" % (
        '%s\n' % ('%02x' * pic.width) * pic.height % tuple(
            17 if i else 0 for i in pic.rgba[0::4]
        )
    )
)
print(
    "  template: '''\n%s\n            '''" % pic.dump()
)
