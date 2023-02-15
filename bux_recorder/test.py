import tkinter as tk
from tkinter import ttk

from frontend.ui_setup import *
from frontend.ui_test_tab2 import *
from frontend.ui_cameras2 import *
from frontend.label_text import *
from frontend.ui_menubar import *


class BuxRecorder(ttk.Frame):
    def __init__(self):
        self.labels = label_text.create_labels()
        self.date = dt.datetime.now().strftime("%Y-%m-%d")
        self.log_object = logger.Create_logger("debugger")
        self.log_object.add_stream_handler()
        self.log = logging.getLogger("debugger")
        self.event_stop = mp.Event()
        self.event_preview = mp.Event()
        self.event_record = mp.Event()
        self.record_running = False
        self.cam_opened = {}
        self.working_serial = self.labels["t_serial_choose"]
        self.serial_opened = False
        self.path = ""
        self.path_short = ""
        self.app = self.GUI()

    def GUI(self):
        """Create the main UI window"""
        self.root = tk.Tk()
        self.logo = tk.PhotoImage(file="bux_recorder/frontend/resources/bux_logo.png")
        self.logo = self.logo.zoom(8)
        self.logo = self.logo.subsample(18)
        self.root.title("Bux Recorder")
        self.root.call("wm", "iconphoto", self.root._w, self.logo)
        self.create_menubar()
        self.root.config(menu=self.menubar)

        # To get button height and width in pixels: https://stackoverflow.com/a/46286221/13240268
        self.colwidth = 360
        self.pad = 25
        self.w, self.h = self.colwidth + 2 * self.pad, 400
        self.gui_coordinates = utils.get_gui_coordinates(self.root, self.w, self.h)
        shift = (0, 0, -100, 0)
        self.gui_coordinates = tuple(
            map(lambda x, y: x + y, self.gui_coordinates, shift)
        )
        self.root.geometry("%dx%d+%d+%d" % self.gui_coordinates)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.root)

        # Create tabs
        self.frame_setup = SetupTab(parent=self.notebook)
        self.frame_cameras = CameraTab(parent=self, toplevel=self.notebook)
        # self.frame_micropython = MicropythonTab(parent=self.notebook)
        # self.frame_experiment = ExperimentTab(parent=self.notebook)

        # Add frames to notebook
        self.notebook.add(self.frame_setup, text="Setup")
        self.notebook.add(self.frame_cameras, text="Cameras")

        # Pack tabs
        self.notebook.pack()

    def create_menubar(self):
        self.menubar = Menu(
            self.root,
            background="#ff8000",
            foreground="black",
            activebackground="white",
            activeforeground="black",
        )
        file = Menu(self.menubar, tearoff=1, background="#ffcc99", foreground="black")
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as")
        file.add_separator()
        file.add_command(label="Exit", command=self.close)
        self.menubar.add_cascade(label="File", menu=file)

        edit = Menu(self.menubar, tearoff=0)
        edit.add_command(label="Undo")
        edit.add_separator()
        edit.add_command(label="Cut")
        edit.add_command(label="Copy")
        edit.add_command(label="Paste")
        self.menubar.add_cascade(label="Edit", menu=edit)

        help = Menu(self.menubar, tearoff=0)
        help.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=help)

    def about():
        messagebox.showinfo(
            "PythonGuides", "Python Guides aims at providing best practical tutorials"
        )

    def close(self):
        if messagebox.askokcancel("Quit", self.labels["t_quit"]):
            self.event_stop.set()
            self.event_preview.clear()
            self.event_record.clear()
            cv2.waitKey(1)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            exit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BuxRecorder()
    app.run()
