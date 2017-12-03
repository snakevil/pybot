# encoding: utf-8

import tkinter as tk

__all__ = ['Modal']

class Modal(tk.Toplevel):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, **kwargs)
        self._parent = parent
        self.title(title)
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.bind('<Escape>', self.close)

    def show(self):
        self.update_idletasks()
        width = max(240, self.winfo_width())
        height = max(120, self.winfo_height())
        width0, height0 = self.maxsize()
        self.geometry(
            '%dx%d+%d+%d' % (
                width,
                height,
                (width0 - width) >> 1,
                (height0 - height) >> 1
            )
        )
        self._parent.wait_window(self)

    def close(self, event = None):
        self.destroy()
