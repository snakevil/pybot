# encoding: utf-8

class Firable(object):
    def __init__(self):
        self._handlers = {}

    def on(self, name, handler, preferred = False):
        if not self._handlers.get(name):
            self._handlers[name] = []
        if callable(handler):
            if preferred:
                self._handlers[name].insert(0, handler)
            else:
                self._handlers[name].append(handler)
        return self

    def fire(self, name, *args):
        try:
            succeed = True
            for handler in self._handlers.get(name) or []:
                result = handler(*args)
                if isinstance(result, tuple) or isinstance(result, list):
                    args = result[1:]
                    succeed = result[0]
                else:
                    succeed = result
                if None != succeed and not succeed:
                    break
            return succeed
        except Exception as e:
            if 'error' == name:
                if __debug__:
                    raise e
                print('fire:', name, self, (*args), e)
            else:
                self.fire('error', e)
            return False
