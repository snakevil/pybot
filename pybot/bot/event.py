# encoding: utf-8

class Event(dict):
    def __init__(self, attrs, *args):
        super(Event, self).__init__(*args)
        self.__attrs = attrs

    def __getattr__(self, name):
        return self.__attrs.get(name)
