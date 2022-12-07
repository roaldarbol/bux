import os
import time
import datetime as dt
import platform
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
import toml
import cv2
import asyncio
import logging
import multiprocessing as mp
import belay

# From the bux package
import label_text as label_text
import utils as utils
import gui_video as gui_video
import serial_connection as serial_connection
import logger as logger

# Functions
class bux_recorder:
    def __init__(self):
        self.labels = label_text.create_labels()
        self.date = dt.datetime.now().strftime("%Y-%m-%d")
        self.log_object = logger.Create_logger("debugger")
        self.log_object.add_stream_handler()
        self.log = logging.getLogger("debugger")
        # self.cam_log = logging.getLogger('camera_log')
        # if utils.is_raspberrypi() == False:
        # self.log.info("You're not on a Raspberry Pi")
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
        self.logo = tk.PhotoImage(file="bux_recorder/locust.png")
        self.logo = self.logo.zoom(8)
        self.logo = self.logo.subsample(18)
        self.root.title("Bux Recorder")
        self.root.call("wm", "iconphoto", self.root._w, self.logo)

        # To get button height and width in pixels: https://stackoverflow.com/a/46286221/13240268
        self.colwidth = 180
        self.pad = 25
        self.w, self.h = self.colwidth + 2 * self.pad, 400
        self.gui_coordinates = utils.get_gui_coordinates(self.root, self.w, self.h)
        shift = (0, 0, -100, 0)
        self.gui_coordinates = tuple(
            map(lambda x, y: x + y, self.gui_coordinates, shift)
        )
        self.root.geometry("%dx%d+%d+%d" % self.gui_coordinates)
        self.root.resizable(0, 0)
        # self.root.bind("<space>", self.toggle_record) # Removed space access to Start Experiment
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        # self.root.columnconfigure(0, minsize=self.col_width)
        # self.root.columnconfigure(1, minsize=20)
        # self.root.columnconfigure(2, minsize=self.col_width)

        """Create GUI Elements"""
        # === TOP PANEL === #
        self.label_title = tk.Label(
            self.root,
            # image=self.logo,
            text="BUX",
            justify=tk.CENTER,
            font=("Avenir", 44)
            # height=70
        )
        self.button_dirname = tk.Button(
            self.root,
            text=self.labels["t_dir_choose"][0],
            width=15,
            command=self.get_dir,
        )

        # === MID PANEL === #
        self.button_window_camera = tk.Button(
            self.root,
            state="disabled",
            text=self.labels["t_cam"],
            width=15,
            command=self.create_window_cam,
        )
        self.button_window_serial = tk.Button(
            self.root,
            state="disabled",
            text=self.labels["t_serial"],
            width=15,
            command=self.create_window_serial,
        )

        # === BOTTOM PANEL === #
        self.button_record = tk.Button(
            self.root,
            state="disabled",
            text=self.labels["t_start"],
            width=15,
            bg="green",
            command=self.toggle_record,
        )
        self.sysinfo = tk.Label(
            self.root, text="OS: " + utils.get_platform(), font=("TkDefaultFont", 8)
        )

        # self.widgets_serial = [
        #     self.text_command,
        #     self.dropdown_scripts,
        #     self.button_send_serial
        # ]

        # for widget in self.widgets_serial:
        #         widget.configure(state='disable')

        """Position elements into grid"""
        # First we assign padding to all widgets
        for widgets in self.root.winfo_children():
            widgets.grid_configure(padx=self.pad, pady=(5, 5))

        # Then customise placement
        self.label_title.grid(row=0, column=0, pady=(30, 30))
        self.button_dirname.grid_configure(row=2, column=0)

        self.button_window_camera.grid(row=3, column=0)
        self.button_window_serial.grid(row=4, column=0)

        self.button_record.grid(row=5, column=0, pady=(40, 20))
        self.sysinfo.grid(row=6, column=0, sticky="sw", pady=25)

        """Bindings"""
        self.button_dirname.bind(
            "<Enter>",
            lambda function: (
                utils.hover(
                    button=self.button_dirname, enter=True, message=self.path_short
                )
            ),
        )
        self.button_dirname.bind(
            "<Leave>",
            lambda function: (
                utils.hover(
                    button=self.button_dirname,
                    enter=False,
                    message=self.labels["t_dir_choose_current"],
                )
            ),
        )

    def create_window_cam(self):
        self.window_cam = gui_video.CameraWindow(
            labels=self.labels,
            coordinates=self.gui_coordinates,
            toplevel=self.root,
            parent=self,
        )

    def create_window_serial(self):
        self.window_serial = serial_connection.SerialWindow(
            labels=self.labels, coordinates=self.gui_coordinates, toplevel=self.root
        )

    def toggle_record(self):
        """Toggles recording Start/Stop state"""
        self.window_cam.toggle_record()

        if self.record_running == False:  # otherwise it starts
            self.window_cam.button_activate.config(state="disable")

        if self.record_running == True:  # if the experiment is running, it stops
            self.button_record.config(text=self.labels["t_start"], bg="green")

        self.record_running = not self.record_running

    def get_dir(self):
        """Ask user to input directory"""
        self.path = tk.filedialog.askdirectory(
            parent=self.root, initialdir="/home/", title=self.labels["t_dir_choose"][0]
        )
        tk.Tk().withdraw()
        if len(self.path) - 20 <= 0:
            cutoff = 0
        else:
            cutoff = len(self.path) - 20
        self.path_short = (self.path[:cutoff] and "..") + self.path[cutoff:]
        self.labels["t_dir_choose_current"] = self.labels["t_dir_choose"][1]
        self.button_dirname.config(text=self.labels["t_dir_choose_current"])
        self.button_window_camera.config(state="normal")
        self.button_window_serial.config(state="normal")
        self.button_record.config(state="normal")
        self.log_object.add_file_handler(self.path, self.date)

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
    app = bux_recorder()
    app.run()
