#!/usr/local/bin/python3
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Root class to create the interface and define the controller function to switch frames
class RootApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(NoteBook)

    # controller function
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# sub-root to contain the Notebook frame and a controller function to switch the tabs within the notebook
class NoteBook(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.notebook = ttk.Notebook()
        self.tab1 = Tab1(self.notebook)
        self.tab2 = Tab2(self.notebook)
        self.tab3 = Tab3(self.notebook)
        self.notebook.add(self.tab1, text="Tab1")
        self.notebook.add(self.tab2, text="Tab2")
        self.notebook.add(self.tab3, text="Tab3")
        self.notebook.pack()

    # controller function
    def switch_tab1(self, frame_class):
        new_frame = frame_class(self.notebook)
        self.tab1.destroy()
        self.tab1 = new_frame


# Notebook - Tab 1
class Tab1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self._frame = None
        self.switch_frame(Tab1_Frame1)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# first frame for Tab1
class Tab1_Frame1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, text="this is a test - one")
        # button object with command to replace the frame
        self.button = Button(
            self, text="Change it!", command=lambda: master.switch_frame(Tab1_Frame2)
        )
        self.label.pack()
        self.button.pack()


# second frame for Tab1
class Tab1_Frame2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, text="it has been changed!")
        # and another button to change it back to the previous frame
        self.button = Button(
            self,
            text="Change it back!",
            command=lambda: master.switch_frame(Tab1_Frame1),
        )
        self.label.pack()
        self.button.pack()


# Notebook - Tab 2
class Tab2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, text="this is a test - two")
        self.label.pack()


# Notebook - Tab 3
class Tab3(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, text="this is a test - three")
        self.label.pack()


if __name__ == "__main__":
    Root = RootApp()
    Root.geometry("640x480")
    Root.title("Frame test")
    Root.mainloop()
