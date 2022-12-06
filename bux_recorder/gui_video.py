import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import multiprocessing as mp
import threading
import datetime as dt
import logging
import cv2
import toml

# Bux sublibraries
import label_text
import utils as utils
import logger as logger
import video as video
import BuxVideo as BuxVideo


class CameraWindow:
    def __init__(self, labels, coordinates, toplevel=None, parent=None):
        self.parent = parent
        if self.parent == None:
            self.path = "/Users/roaldarbol/Desktop"
            self.event_stop = mp.Event()
            self.event_preview = mp.Event()
            self.event_record = mp.Event()
        if self.parent is not None:
            for key, val in vars(self.parent).items():
                setattr(self, key, val)
        else:
            self.labels = labels
            self.date = self.date = dt.datetime.now().strftime("%Y-%m-%d")
        self.log = logging.getLogger("debugger")

        if toplevel is None:
            self.window_camera = tk.Tk()
        else:
            self.window_camera = tk.Toplevel(toplevel)

        self.window_camera.title("Cameras")

        # sets the geometry of toplevel
        self.cam_queue = mp.Queue()
        self.working_cams = [self.labels["t_cam_choose"]]
        self.preview_running = False
        self.record_running = False
        self.active = False

        self.video_format = {
            "avi": cv2.VideoWriter_fourcc(*"XVID"),
            #'mp4': cv2.VideoWriter_fourcc(*'H264'),
            "mp4": cv2.VideoWriter_fourcc(*"XVID"),
        }

        self.default_cam_resolutions = [
            "640, 480",
            "800, 600",
            "1280, 720",
            "1920, 1280",
        ]

        self.cam_resolution_pre = {}
        self.cam_resolutions = {}
        self.cam_settings = {}
        self.generic_settings = {
            "res_width": 800,
            "res_height": 600,
            "vid_interval": 360,
        }

        self.update_cams()
        self.get_camera_params()

        self.colwidth = 180
        self.pad = 10
        self.cam_n = len(self.working_cams)
        self.w, self.h = self.colwidth * self.cam_n + self.pad * 2 * self.cam_n, 350
        self.x, self.y = coordinates[2] + coordinates[0] + 10, coordinates[3]
        self.window_coord = self.w, self.h, self.x, self.y
        self.window_camera.geometry("%dx%d+%d+%d" % self.window_coord)
        if self.parent == None:
            self.window_camera.protocol("WM_DELETE_WINDOW", self.close)

        # For all cams
        self.button_activate = tk.Button(
            self.window_camera,
            state="disable",
            text=self.labels["t_cam_activate"],
            width=15,
            command=self.toggle_activate,
        )
        self.button_preview = tk.Button(
            self.window_camera,
            state="disable",
            text=self.labels["t_preview"],
            width=15,
            command=self.toggle_preview,
        )

        # --- CREATE WIDGET DICTS --- #
        self.cap = {}
        self.cams_selected = {}
        self.cams_enabled = {}
        self.dropdown_camera = {}
        self.button_open_camera = {}
        self.dropdown_resolution = {}
        self.spinbox_hour = {}
        self.spinbox_min = {}
        self.button_settingsname = {}
        self.button_loadsettings = {}
        self.settings_path = {}
        self.settings_path_short = {}

        # --- CREATE WIDGETS FOR EACH CAMERA --- #
        for cam in self.working_cams:
            self.cams_selected[cam] = False
            self.cam_settings[cam] = self.generic_settings
            self.settings_path[cam] = ""
            self.settings_path_short[cam] = ""

            # Define lambda functions
            toggle_cam_func = lambda x=cam: self.toggle_camera(x)
            settings_choose = lambda x=cam: self.get_file(x)
            settings_load = lambda x=cam: self.load_settings(x)

            self.dropdown_camera[cam] = ttk.Combobox(
                self.window_camera,
                state="readonly",
                justify=tk.CENTER,
                width=16,
                values=self.working_cams,
            )
            self.dropdown_camera[cam].current(cam)
            self.button_open_camera[cam] = tk.Button(
                self.window_camera,
                text=self.labels["t_cam_select"],
                width=15,
                command=toggle_cam_func,
            )
            self.dropdown_resolution[cam] = ttk.Combobox(
                self.window_camera,
                state="readonly",
                justify=tk.CENTER,
                width=16,
                values=self.cam_resolutions[cam],
            )
            ind = self.cam_resolutions[cam].index(self.cam_resolution_pre[cam])
            self.dropdown_resolution[cam].current(ind)
            # self.spinbox_hour[cam] = tk.Spinbox(
            #     self.window_camera,
            #     from_ = 0,
            #     to = 24,
            #     justify=tk.CENTER,
            #     width=15,
            # )
            self.spinbox_min[cam] = tk.Spinbox(
                self.window_camera,
                from_=0,
                to=24 * 60,
                justify=tk.CENTER,
                width=15,
                textvariable=tk.DoubleVar(self.window_camera, 360),
            )
            self.button_settingsname[cam] = tk.Button(
                self.window_camera,
                text=self.labels["t_settings_choose"][0],
                width=15,
                command=settings_choose,
            )
            self.button_loadsettings[cam] = tk.Button(
                self.window_camera,
                text=self.labels["t_settings_load"],
                width=15,
                command=settings_load,
            )

            self.dropdown_camera[cam].grid_configure(
                row=0, column=cam, pady=(20, 0), sticky="e"
            )
            self.button_open_camera[cam].grid(row=1, column=cam, sticky="e")
            self.button_settingsname[cam].grid(row=2, column=cam, sticky="e")
            self.button_loadsettings[cam].grid(row=3, column=cam, sticky="e")
            self.dropdown_resolution[cam].grid_configure(row=4, column=cam, sticky="e")
            # self.spinbox_hour[cam].grid(row=5, column=cam, sticky="e")
            self.spinbox_min[cam].grid(row=6, column=cam, pady=(7, 0), sticky="e")

            # Bindings
            lambda_settings_enter = lambda function, x=cam: utils.hover(
                button=self.button_settingsname[x],
                enter=True,
                message=self.settings_path_short[x],
            )
            lambda_settings_leave = lambda function, x=cam: utils.hover(
                button=self.button_settingsname[x],
                enter=False,
                message=self.labels["t_settings_choose_current"][x],
            )

            self.button_settingsname[cam].bind("<Enter>", lambda_settings_enter)
            self.button_settingsname[cam].bind("<Leave>", lambda_settings_leave)

        for widgets in self.window_camera.winfo_children():
            widgets.grid_configure(padx=self.pad)  # , pady=(2))
        self.button_activate.grid(row=7, column=0, pady=(20, 5), columnspan=self.cam_n)
        self.button_preview.grid(row=8, column=0, pady=(0, 5), columnspan=self.cam_n)

        if self.parent == None:
            self.button_record = tk.Button(
                self.window_camera,
                state="disable",
                text=self.labels["t_start"],
                width=15,
                command=self.toggle_record,
            )
            self.button_record.grid(row=9, column=0, pady=(0, 5), columnspan=self.cam_n)

        # """Disable camera buttons"""
        # widgets_cam_enable = [
        #     button_preview,
        #     # button_start
        # ]
        # widgets_cam_disable = [
        #     button_loadsettings,
        #     button_preview,
        #     # button_start
        # ]

        # # Bindings
        # for widget in widgets_cam_disable:
        #         widget.configure(state='disable')

    def update_cams(self):
        self.working_cams = []
        [
            self.available_cams,
            self.working_cams,
            self.non_working_cams,
        ] = self.list_ports()
        self.working_cams_original = self.working_cams.copy()
        for cam in self.working_cams:
            self.cam_settings[cam] = self.generic_settings
            cap = cv2.VideoCapture(cam)
            h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            cap.release()
            self.cam_settings[cam]["res_height"] = h
            self.cam_settings[cam]["res_width"] = w
            # self.cam_settings[cam]['res_width'] = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            # w = self.cam_settings[cam]['res_width']
            # h = self.cam_settings[cam]['res_height']

    def get_camera_params(self):
        for cam in self.working_cams:
            self.cam_resolutions[cam] = self.default_cam_resolutions
            h = self.cam_settings[cam]["res_height"]
            w = self.cam_settings[cam]["res_width"]
            resolution = str(int(w)) + ", " + str(int(h))
            self.cam_resolution_pre[cam] = resolution
            if resolution not in self.cam_resolutions[cam]:
                self.cam_resolutions[cam] = [resolution] + self.cam_resolutions[cam]

    def toggle_camera(self, cam):
        if not self.cams_selected[cam]:
            self.cams_selected[cam] = True
            self.dropdown_camera[cam].config(state="disabled")
            self.button_open_camera[cam].config(text=self.labels["t_cam_deselect"])
            self.log.info("Camera %s selected", cam)
        elif self.cams_selected[cam]:
            self.cams_selected[cam] = False
            self.dropdown_camera[cam].config(state="readonly")
            self.button_open_camera[cam].config(text=self.labels["t_cam_select"])
            self.log.info("Camera %s deselected", cam)
        if any(self.cams_selected.values()):
            self.button_activate.config(state="normal")
        else:
            self.button_activate.config(state="disabled")

    def toggle_activate(self):
        """Toggles Preview Start/Stop state"""

        if self.active == False:  # otherwise it starts
            for cam in self.cams_selected:
                self.button_open_camera[cam].config(state="disabled")
            self.button_activate.config(text=self.labels["t_cam_deactivate"], bg="red")
            self.button_preview.config(state="normal", bg="green")
            if self.parent == None:
                self.button_record.config(state="normal", bg="green")

            ### MP IMPLEMENTATION
            self.processes = {}
            self.cams_to_open = {
                k: v for k, v in enumerate(self.cams_selected.values()) if v == True
            }

            # Spawn processes
            self.start_dt = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
            for cam in self.cams_to_open:
                self.processes[cam] = mp.Process(
                    target=BuxVideo.BuxCamera,
                    args=[
                        cam,
                        self.cam_queue,
                        self.path,
                        self.start_dt,
                        self.event_stop,
                        self.event_preview,
                        self.event_record,
                    ],
                )

            # Start processes
            for p in self.processes:
                self.processes[p].start()
                self.log.info("Process %s started" % p)

        if self.active == True:
            self.event_stop.set()
            for p in self.processes:
                self.processes[p].join()
            # cv2.destroyAllWindows() # Just needs any input, though it's not using it here...
            for cam in self.cams_selected:
                self.button_open_camera[cam].config(state="normal")
            self.button_activate.config(text=self.labels["t_cam_activate"], bg="green")
            self.button_preview.config(state="disable", bg="green")
            if self.parent == None:
                self.button_record.config(state="disable", bg="green")
            self.event_stop.clear()
            # self.button_start.config(state="normal")

        self.active = not self.active
        # print(self.cam_queue.get('foo'))

    def toggle_preview(self):
        """Toggles Preview Start/Stop state"""
        if self.preview_running == False:  # otherwise it starts

            # Add settings
            for cam in self.cams_to_open:
                res = self.dropdown_resolution[cam].get()
                res = res.split(",")
                res = [int(n) for n in res]
                self.cam_settings[cam]["res_width"] = res[0]
                self.cam_settings[cam]["res_height"] = res[1]
                self.cam_queue.put(self.cam_settings)

            # Set buttons
            self.button_preview.config(text=self.labels["t_preview_stop"], bg="red")
            self.button_activate.config(state="disable")

            # Begin preview
            self.event_preview.set()

        if self.preview_running == True:  # if the experiment is running, it stops
            for cam in self.cams_to_open:
                temp_settings = self.cam_queue.get()
                self.cam_settings[cam] = temp_settings[cam]
            self.event_preview.clear()
            self.button_preview.config(text=self.labels["t_preview"], bg="green")
            self.button_activate.config(state="normal")

        self.preview_running = not self.preview_running
        # print(self.cam_queue.get('foo'))

    def toggle_record(self):
        """Toggles Preview Start/Stop state"""
        if self.record_running == False:  # otherwise it starts

            # Add settings
            for cam in self.cams_to_open:
                res = self.dropdown_resolution[cam].get()
                res = res.split(",")
                res = [int(n) for n in res]
                self.cam_settings[cam]["res_width"] = res[0]
                self.cam_settings[cam]["res_height"] = res[1]
                self.cam_settings[cam]["vid_interval"] = int(
                    self.spinbox_min[cam].get()
                )
                self.cam_queue.put(self.cam_settings)

            # Set buttons
            self.button_record.config(text=self.labels["t_stop"], bg="red")
            self.button_activate.config(state="disable")
            self.event_record.set()

        if self.record_running == True:  # if the experiment is running, it stops
            for cam in self.cams_to_open:
                temp_settings = self.cam_queue.get()
                self.cam_settings[cam] = temp_settings[cam]
            self.event_record.clear()
            self.button_record.config(text=self.labels["t_start"], bg="green")
            self.button_activate.config(state="normal")

        self.record_running = not self.record_running
        # print(self.cam_queue.get('foo'))

    def list_ports(self):
        """
        Test the ports and returns a tuple with the available ports and the ones that are working.
        """
        non_working_ports = []
        dev_port = 0
        working_ports = []
        available_ports = []
        while (
            len(non_working_ports) < 6
        ):  # if there are more than 5 non working ports stop the testing.
            camera = cv2.VideoCapture(dev_port)
            if not camera.isOpened():
                non_working_ports.append(dev_port)
                # print("Port %s is not working." %dev_port)
            else:
                is_reading, img = camera.read()
                w = camera.get(3)
                h = camera.get(4)
                if is_reading:
                    # print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                    working_ports.append(dev_port)
                else:
                    # print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                    available_ports.append(dev_port)
            dev_port += 1
        return available_ports, working_ports, non_working_ports

    def check_cv_break(self, cams_selected):
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return True
        elif not any(cams_selected):
            return True

    def get_file(self, cam):
        self.settings_path[cam] = tk.filedialog.askopenfilename(
            parent=self.window_camera,
            initialdir="/home/",
            title=self.t_settings_choose[0],
        )
        tk.Tk().withdraw()
        if len(self.settings_path[cam]) - 20 <= 0:
            cutoff = 0
        else:
            cutoff = len(self.settings_path[cam]) - 20
        self.settings_path_short[cam] = (
            self.settings_path[cam][:cutoff] and ".."
        ) + self.settings_path[cam][cutoff:]
        self.t_settings_choose_current[cam] = self.t_settings_choose[1]
        self.button_settingsname[cam].config(text=self.t_settings_choose_current[cam])
        self.button_loadsettings[cam].configure(state="normal")

    def load_settings(self, cam):
        self.cam_settings[cam] = toml.load(self.cam_settings_path[cam])
        for key, value in self.cam_settings[cam].items():
            cv_key = "cv2." + key
            print(cv_key, value)
            self.cap[cam].set(eval(cv_key), value)
            print(self.cap[cam].get(eval(cv_key)))

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
        self.window_camera.mainloop()


if __name__ == "__main__":
    mp.freeze_support()
    app = CameraWindow(label_text.create_labels(), [200, 100, 100, 100])
    app.run()
