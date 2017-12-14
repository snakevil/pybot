# encoding: utf-8

import tkinter as tk

import sys
import platform
from os import path

from .. import core

__all__ = ['App']

class App(core.Firable):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__()
        self.window = tk.Tk(*args, **kwargs)
        self.window.protocol('WM_DELETE_WINDOW', lambda: self.fire('close'))
        self.platform = platform.system()
        self.prefix = sys.prefix if hasattr(sys, 'frozen') \
            else path.dirname(path.realpath(sys.argv[0]))
        self.id = path.basename(sys.argv[0]).split('.')[0]

        self._debug = None

        self.on('close', lambda: self.window.quit())

        def on_error(error):
            raise error
        self.on('error', on_error)

    @classmethod
    def bundle(cls):
        return '%s.%s' % (cls.__module__, cls.__name__)

    @staticmethod
    def version():
        return (1, 0, 0, 0)

    def run(self):
        self.window.mainloop()

    def debug(self, value = None):
        if None != value:
            debug = bool(value)
            if debug != self._debug:
                self._debug = debug
                self.fire('debug', debug)
        return self._debug
