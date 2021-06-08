# -*- coding: utf-8 -*-

from tkinter import *


class Scrollable(Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame, 
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16, bg="white"):
        scrollbar = Scrollbar(frame, width=width)
        scrollbar.pack(side=LEFT, fill=Y, expand=False)

        self.canvas = Canvas(frame, yscrollcommand=scrollbar.set, background=bg)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind("<Configure>", self.__fill_canvas)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # base class initialization
        Frame.__init__(self, frame)         

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0, 0, window=self, anchor=NW)

    def __fill_canvas(self, event):
        """ Enlarge the windows item to the canvas width """

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width=canvas_width)        

    def update(self):
        """ Update the canvas and the scrollregion """

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))

    def on_mousewheel(self, event):
        """ Scroll """

        self.canvas.yview_scroll(int(-1*(event.delta/100)), "units")


"""
frame = Frame(self._ROOT)
frame.place(relx=0.5, rely=0.5)

scrollable_body = Scrollable(frame)

for num in range(30):
    Label(scrollable_body, text=f"{num}. frame").grid(row=num, column=0)
    Button(scrollable_body, text=f"{num}. button").grid(row=num, column=1)

scrollable_body.update()
"""
