from tkinter import *
from tkinter import messagebox

ws = Tk()
ws.title("Python Guides")
ws.geometry("300x250")


def about():
    messagebox.showinfo(
        "PythonGuides", "Python Guides aims at providing best practical tutorials"
    )


def darkMode():
    if darkmode.get() == 1:
        ws.config(background="black")
    elif darkmode.get() == 0:
        ws.config(background="white")
    else:
        messagebox.showerror("PythonGuides", "Something went wrong!")


menubar = Menu(
    ws,
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
file.add_command(label="Exit", command=ws.quit)
menubar.add_cascade(label="File", menu=file)

edit = Menu(menubar, tearoff=0)
edit.add_command(label="Undo")
edit.add_separator()
edit.add_command(label="Cut")
edit.add_command(label="Copy")
edit.add_command(label="Paste")
menubar.add_cascade(label="Edit", menu=edit)

minimap = BooleanVar()
minimap.set(True)
darkmode = BooleanVar()
darkmode.set(False)

view = Menu(menubar, tearoff=0)
view.add_checkbutton(label="show minimap", onvalue=1, offvalue=0, variable=minimap)
view.add_checkbutton(
    label="Darkmode", onvalue=1, offvalue=0, variable=darkmode, command=darkMode
)
menubar.add_cascade(label="View", menu=view)

help = Menu(menubar, tearoff=0)
help.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=help)

ws.config(menu=menubar)
ws.mainloop()
