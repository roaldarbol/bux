from tkinter import *
from tkinter import messagebox


class MenuBar:
    def __init__(self, parent):
        menubar = Menu(
            parent,
            background="#ff8000",
            foreground="black",
            activebackground="white",
            activeforeground="black",
        )
        file = Menu(menubar, tearoff=1, background="#ffcc99", foreground="black")
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as")
        file.add_separator()
        file.add_command(label="Exit", command=parent.quit)
        menubar.add_cascade(label="File", menu=file)

        edit = Menu(menubar, tearoff=0)
        edit.add_command(label="Undo")
        edit.add_separator()
        edit.add_command(label="Cut")
        edit.add_command(label="Copy")
        edit.add_command(label="Paste")
        menubar.add_cascade(label="Edit", menu=edit)

        help = Menu(menubar, tearoff=0)
        help.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=help)

    def about():
        messagebox.showinfo(
            "PythonGuides", "Python Guides aims at providing best practical tutorials"
        )
