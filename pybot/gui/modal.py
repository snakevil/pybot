# encoding: utf-8

import tkinter as tk

__all__ = ['Modal']

class Modal(tk.Toplevel):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.bind('<Escape>', self.close)

    def close(self, event = None):
        self.destroy()
