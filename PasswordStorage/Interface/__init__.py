# -*- coding: utf-8 -*-

from tkinter import *
from win32api import GetSystemMetrics


WINDOW_TITLE = "Password Storage"
WINDOW_ICON = None

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

WINDOW_MINSIZE_WIDTH = 400
WINDOW_MINSIZE_HEIGHT = 300

SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)

WINDOW_GEOMETRY = "%(win_width)sx%(win_height)s+%(width)s+%(height)s" % {
    "win_width": WINDOW_WIDTH,
    "win_height": WINDOW_HEIGHT,
    "width": int((SCREEN_WIDTH/2) - (WINDOW_WIDTH/2)),
    "height": int((SCREEN_HEIGHT/2) - (WINDOW_HEIGHT/2))
}


class Interface:
    def __init__(self):
        self._ROOT = Tk()

        self._ROOT.title(WINDOW_TITLE)
        self._ROOT.iconbitmap(default=WINDOW_ICON)
        self._ROOT.geometry(WINDOW_GEOMETRY)
        self._ROOT.minsize(width=WINDOW_MINSIZE_WIDTH, height=WINDOW_MINSIZE_HEIGHT)

    def start_interface(self):
        self._ROOT.mainloop()
