# encoding: utf-8

from .expect import Base, Expect

class Negative(Expect):
    def __init__(self, positive, **spots):
        assert isinstance(positive, Base)
        super(Negative, self).__init__(**spots)
        self._expect = positive
        self.spots.update(positive.spots)

    def __repr__(self):
        return 'Negative(%r)' % self._expect

    def test(self, event):
        return not self._expect.test(event)
