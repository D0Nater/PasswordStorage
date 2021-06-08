# -*- coding: utf-8 -*-

from tkinter import *
from win32api import GetSystemMetrics

from .account_manage import AccountManage
from .profiles_manage import ProfilesManage


WINDOW_TITLE = "Password Storage"
WINDOW_ICON = None

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 400

WINDOW_MINSIZE_WIDTH = 400
WINDOW_MINSIZE_HEIGHT = 300

SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)

WINDOW_GEOMETRY = "%(win_width)sx%(win_height)s+%(win_pos_x)s+%(win_pos_y)s" % {
    "win_width": WINDOW_WIDTH,
    "win_height": WINDOW_HEIGHT,
    "win_pos_x": int((SCREEN_WIDTH/2) - (WINDOW_WIDTH/2)),
    "win_pos_y": int((SCREEN_HEIGHT/2) - (WINDOW_HEIGHT/2))
}


class Interface(AccountManage, ProfilesManage):
    def __init__(self, account_control, profiles_db_control):
        self._ACCOUNT_CONTROL = account_control
        self._PROFILES_DB_CONTROL = profiles_db_control

        self._ROOT = Tk()
        self._HEAD_FRAME = Frame(self._ROOT, height=55)
        self._MAIN_FRAME = Frame(self._ROOT)
        self._PROFILES_FRAME = Frame(self._ROOT)

        self._ROOT.title(WINDOW_TITLE)
        self._ROOT.iconbitmap(default=WINDOW_ICON)
        self._ROOT.geometry(WINDOW_GEOMETRY)
        self._ROOT.minsize(width=WINDOW_MINSIZE_WIDTH, height=WINDOW_MINSIZE_HEIGHT)

        self._HEAD_FRAME.pack(fill="both", side=TOP)
        self._MAIN_FRAME.pack(fill="both", expand=True)

    def start_interface(self):
        self._ROOT.mainloop()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
