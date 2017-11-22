# encoding: utf-8

from pybot.bot import expect

class Retry(expect.Fingerprint):
    def __init__(self):
        super(Retry, self).__init__(
            ((296, 182), (363, 198)),
            'bfabbababaaaba2b',
            154,
            ok = (((418, 250), (530, 292)), 5),
            cancel = (((270, 250), (382, 292)), 5)
        )

    def __str__(self):
        return '失败重试'
