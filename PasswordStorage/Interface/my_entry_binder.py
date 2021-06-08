# -*- coding: utf-8 -*-


class MyEntryBinder:
    @staticmethod
    def on_entry_click(event, entry, text, show=""):
        if entry.get() == text:
           entry.delete(0, "end")
           entry.insert(0, "")
           entry.config(fg="black", show=show)

    @staticmethod
    def on_focusout(event, entry, text, show=""):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey", show=show)

    @staticmethod
    def bind_entry(entry, text, show=""):
        entry.insert(0, text)
        entry.bind("<FocusIn>", lambda event: MyEntryBinder.on_entry_click(event, entry, text, show))
        entry.bind("<FocusOut>", lambda event: MyEntryBinder.on_focusout(event, entry, text))
        entry.config(fg="grey")
