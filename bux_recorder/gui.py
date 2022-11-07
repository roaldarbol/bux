import os
import time
import datetime as dt
import platform
import serial
from serial.tools import list_ports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
import toml
import cv2
from serial_mailman.mailman import MailMan
import asyncio
import logging
import multiprocessing as mp

# From the bux package
import bux_recorder.label_text as label_text
import bux_recorder.utils as utils
import bux_recorder.gui_video as gui_video
import bux_recorder.video as video
import bux_recorder.serial_connection as serial_connection
import bux_recorder.logger as logger

# Functions
class bux_recorder():
    def __init__(self):
        self.labels = label_text.create_labels()
        self.date = dt.datetime.now().strftime("%Y-%m-%d")
        self.log_object = logger.Create_logger('debugger')
        self.log_object.add_stream_handler()
        self.log = logging.getLogger('debugger')
        # self.cam_log = logging.getLogger('camera_log')
        # if utils.is_raspberrypi() == False:
        # self.log.info("You're not on a Raspberry Pi")
        self.running = False
        self.cam_opened = {}
        self.working_serial = self.labels["t_serial_choose"]
        self.serial_opened = False
        self.path = ""
        self.path_short = ""
        self.app = self.GUI()
        


    def GUI(self):
        """ Create the main UI window"""
        self.root = tk.Tk()
        self.logo = tk.PhotoImage(file="bux_recorder/locust.png")
        self.logo = self.logo.zoom(8)
        self.logo = self.logo.subsample(18)
        self.root.title('Bux Recorder')
        self.root.call('wm', 'iconphoto', self.root._w, self.logo)
        
        # To get button height and width in pixels: https://stackoverflow.com/a/46286221/13240268
        self.colwidth = 180
        self.pad = 25
        self.w, self.h = self.colwidth + 2*self.pad, 400
        self.gui_coordinates = utils.get_gui_coordinates(self.root, self.w, self.h)
        shift = (0,0,-100,0)
        self.gui_coordinates = tuple(map(lambda x, y: x + y, self.gui_coordinates, shift))
        self.root.geometry('%dx%d+%d+%d' % self.gui_coordinates)
        self.root.resizable(0, 0)
        # self.root.bind("<space>", self.toggle) # Removed space access to Start Experiment
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
            text = self.labels["t_dir_choose"][0], 
            width=15,
            command = self.get_dir
            )

        # === MID PANEL === #
        self.button_window_camera = tk.Button(
            self.root, 
            text = self.labels["t_cam"], 
            width=15,
            command = self.create_window_cam
            )
        self.button_window_serial = tk.Button(
            self.root, 
            text = self.labels["t_serial"], 
            width=15,
            command = self.create_window_serial
            )
        
        # === BOTTOM PANEL === #
        self.button_start = tk.Button(
            self.root, 
            text=self.labels["t_start"],
            width=15,
            bg = "green",
            command = self.toggle
            )
        self.sysinfo = tk.Label(
            self.root,
            text="OS: " + utils.get_platform(),
            font=('TkDefaultFont', 8)
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
            widgets.grid_configure(padx=self.pad, pady=(5,5))
        
        # Then customise placement
        self.label_title.grid(row=0, column=0, pady=(30,30))
        self.button_dirname.grid_configure(row=2, column=0)

        self.button_window_camera.grid(row=3, column=0)
        self.button_window_serial.grid(row=4, column=0)
        
        self.button_start.grid(row=5, column=0, pady=(40,20))
        self.sysinfo.grid(row=6, column=0, sticky="sw", pady=25)
        
        

        """Bindings"""
        self.button_dirname.bind(
            "<Enter>", 
            lambda function: (
                utils.hover(
                    button=self.button_dirname, 
                    enter=True, 
                    message=self.path_short
                )
            )
        )
        self.button_dirname.bind(
            "<Leave>", 
            lambda function: (
                utils.hover(
                    button=self.button_dirname, 
                    enter=False, 
                    message=self.labels["t_dir_choose_current"]
                )
            )
        )

    def create_window_cam(self):
        self.window_cam = gui_video.CameraWindow(
            labels=self.labels, 
            coordinates=self.gui_coordinates,
            toplevel=self.root,
            parent=self
            )
    
    def create_window_serial(self):
        self.window_serial = serial_connection.SerialWindow(
            labels=self.labels, 
            coordinates=self.gui_coordinates,
            toplevel=self.root
            )

    def toggle(self):
        """Toggles Start/Stop state"""
        if self.running == False: # otherwise it starts
            # self.ser = serial_connection.serial_connection("usb")
            # self.ser.connect_device()
            self.start_dt = dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
            # if self.path != "":
            #     self.vid_name = "{}/{}".format(self.path, self.start_dt)
            # else:
            #     self.vid_name = self.start_dt
            self.button_start.config(text = self.labels["t_stop"], bg="red")
            self.window_cam.button_preview.config(state="disabled")
            self.start_cams()
            # self.experimental_loop()
            # self.out.release()
            self.root.update()
        
        if self.running == True: # if the experiment is running, it stops
            # bux.experiment.close()
            # cv2.destroyAllWindows()
            self.terminate_cams()
            self.button_start.config(text=self.labels["t_start"], bg="green")
            self.window_cam.button_preview.config(state="normal")
            # self.ser.close()
            # print("Serial disconnected")
        
        self.running = not self.running

    def start_cams(self):
        """Toggles Recording Start/Stop state"""

        ### MP IMPLEMENTATION
        self.processes = {}
        self.cams_to_open = {k:v for k,v in enumerate(self.window_cam.cams_selected.values()) if v == True}
        self.stop = mp.Event()

        # Add settings
        for cam in self.cams_to_open:
            res =  self.window_cam.dropdown_resolution[cam].get()
            res = res.split(',')
            res = [int(n) for n in res]
            self.window_cam.cam_settings[cam]['res_width'] = res[0]
            self.window_cam.cam_settings[cam]['res_height'] = res[1]

        # Spawn processes
        for cam in self.cams_to_open:
            self.window_cam.cam_queue.put(self.window_cam.cam_settings[cam])
            self.processes[cam] = mp.Process(
                target=video.cam_record, 
                args=(
                    cam, 
                    self.window_cam.cam_queue, 
                    self.path,
                    self.start_dt,
                    self.stop
                    ),
                kwargs={
                    "resolution" : self.window_cam.dropdown_resolution[cam].get()
                    }
                )

        # Start processes
        for p in self.processes:
            self.processes[p].start()
            self.log.info("Process %s started" % p)

    def terminate_cams(self):
        self.stop.set()
        for p in self.processes:
            self.window_cam.cam_settings[p] = self.window_cam.cam_queue.get()
            self.processes[p].join()
        
        # cv2.destroyAllWindows() # Just needs any input, though it's not using it here...
        # self.button_start.config(state="normal")
    
    # def experimental_loop(self):
    #     """Initiates the experimental loop"""
    #     self.start_dt = dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    #     # INSERT ERROR STUFF IF PATH DOESN'T EXIST
    #     self.videoname = {}
    #     self.csvname = {}
    #     self.fps = {}
    #     self.vid_width = {}
    #     self.vid_height = {}
    #     self.fourcc = {}
    #     self.out = {}
    #     print(self.window_cam.cap)
    #     for cap in self.window_cam.cap:
    #         print(self.window_cam.cap[cap])
    #         self.videoname[cap] = os.path.join(self.path, '%s_cam-%s.avi'%(self.start_dt, cap))
    #         self.csvname[cap] = os.path.join(self.path, '%s_cam-%s.csv'%(self.start_dt, cap))
    #         print(self.videoname[cap])
    #         print(dt.datetime.now())
        
    #         # Get the width and height of frame
    #         self.fps[cap] = int(self.window_cam.cap[cap].get(cv2.CAP_PROP_FPS))
    #         self.vid_width[cap] = int(self.window_cam.cap[cap].get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    #         self.vid_height[cap] = int(self.window_cam.cap[cap].get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

    #         # # Define the codec and create VideoWriter object
    #         self.fourcc[cap] = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
    #         self.out[cap] = cv2.VideoWriter(
    #             self.videoname[cap], 
    #             self.fourcc[cap], 
    #             self.fps[cap], 
    #             (self.vid_width[cap], self.vid_height[cap])
    #             )
    #         print(self.fourcc[cap],self.fps[cap], self.vid_width[cap], self.vid_height[cap])

    #     # # Create txt or csv file here
    #     i = 0
    #     while self.running:
    #         for cap in self.window_cam.cap:
    #             # print(dt.datetime.now(), "%s"%(cap))
    #             video.read_frame(self.window_cam.cap[cap], out = self.out[cap])
    #             self.cam_log.info("Cam %s: Frame %s", cap, i)
    #             i[cam] += 1
    #         if video.check_cv_break(self.window_cam.cam_opened):
    #             break
    #         self.root.update() # Needed to process new events

    
    def get_dir(self):
        """Ask user to input directory"""
        self.path = tk.filedialog.askdirectory(
            parent=self.root,
            initialdir="/home/",
            title=self.labels["t_dir_choose"][0])
        tk.Tk().withdraw()
        if (len(self.path) - 20 <= 0):
            cutoff = 0
        else: 
            cutoff = len(self.path) - 20
        self.path_short = (self.path[:cutoff] and '..') + self.path[cutoff:] 
        self.labels["t_dir_choose_current"] = self.labels["t_dir_choose"][1]
        self.button_dirname.config(text=self.labels["t_dir_choose_current"])
        self.log_object.add_file_handler(self.path, self.date)
    
    def close(self):
        if messagebox.askokcancel("Quit", self.labels["t_quit"]):
            if any(self.cam_opened):
                for cam in self.cam_opened:
                    if cam:
                        cam = False
                        self.cap[cam].release()
            cv2.destroyAllWindows()
            exit()
        

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = bux_recorder()
    app.run()