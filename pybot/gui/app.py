# encoding: utf-8

import tkinter as tk

import sys
from os import path

__all__ = ['App']

class App(object):
    def __init__(self):
        self.gui = tk.Tk()
        self.on_close(self._on_close)
        self.prefix = sys.prefix if hasattr(sys, 'frozen') \
            else path.dirname(path.realpath(sys.argv[0]))

    def _on_close(self):
        self.gui.quit()

    @staticmethod
    def version():
        return (1, 0, 0)

    def run(self):
        self.gui.mainloop()

    def on_close(self, handler):
        self.gui.protocol('WM_DELETE_WINDOW', handler)