# encoding: utf-8

class Base(object):
    def __repr__(self):
        return '%s()' % type(self).__name__

    def __and__(self, another):
        assert False

    def __iand__(self, another):
        return self.__and__(another)

    def __or__(self, another):
        assert False

    def __ior__(self, another):
        return self.__or__(another)

    def test(self, event):
        return False
