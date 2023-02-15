import tkinter as tk
from tkinter import ttk


class Tab2(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        shell_frame = tk.LabelFrame(self, text="Sample Label Frame", padx=5, pady=5)
        shell_frame.grid(row=0, column=0, padx=5, pady=5)
