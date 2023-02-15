import tkinter as tk
from tkinter import ttk


class SetupTab(ttk.Frame):
    def __init__(self, labels, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
