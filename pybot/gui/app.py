# encoding: utf-8

import tkinter as tk

import sys
import platform
from os import path

__all__ = ['App']

class App(object):
    def __init__(self):
        self.gui = tk.Tk()
        self.gui.protocol('WM_DELETE_WINDOW', self._on_close)
        self.platform = platform.system()
        self.prefix = sys.prefix if hasattr(sys, 'frozen') \
            else path.dirname(path.realpath(sys.argv[0]))
        self.id = path.basename(sys.argv[0]).split('.')[0]
        self._debug = False

    def _on_close(self):
        self.gui.quit()

    def _on_debug(self, value):
        pass

    @classmethod
    def bundle(cls):
        return '%s.%s' % (cls.__module__, cls.__name__)

    @staticmethod
    def version():
        return (1, 0, 0, 0)

    def run(self):
        self.gui.mainloop()

    def debug(self, value = None):
        if None != value:
            debug = bool(value)
            if debug != self._debug:
                self._debug = debug
                self._on_debug(debug)
        return self._debug
