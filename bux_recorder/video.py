import tkinter as tk
from tkinter import ttk
import cv2
import label_text
import bux_recorder.utils as utils

class CameraWindow():
    def __init__(self, labels, coordinates, toplevel=None):
        self.labels = labels
        if toplevel is None:
            self.window_camera = tk.Tk()
        else:
            self.window_camera = tk.Toplevel(toplevel)
            
        self.window_camera.title("Cameras")
    
        # sets the geometry of toplevel
        self.working_cams = [self.labels["t_cam_choose"]]
        self.preview_running = False
        self.update_cams()
        self.colwidth = 180
        self.pad = 10
        self.cam_n = len(self.working_cams)
        self.w, self.h = self.colwidth*self.cam_n + self.pad*2*self.cam_n, 220
        self.x, self.y = coordinates[2] + coordinates[0] + 10, coordinates[3]
        self.window_coord = self.w, self.h, self.x, self.y
        self.window_camera.geometry('%dx%d+%d+%d' % self.window_coord)
        
        # For all cams
        self.button_preview = tk.Button(self.window_camera,
                state="disable",
                text=self.labels["t_preview"],
                width=15,
                command = self.toggle_preview)
        

        # --- CREATE WIDGET DICTS --- #
        self.cap = {}
        self.cam_opened = {}
        self.dropdown_camera = {}
        self.button_open_camera = {}
        self.button_settingsname = {}
        self.button_loadsettings = {}
        self.settings_path = {}
        self.settings_path_short = {}

        # --- CREATE WIDGETS FOR EACH CAMERA --- #
        for cam in self.working_cams:
            self.cam_opened[cam] = False
            self.settings_path[cam] = ""
            self.settings_path_short[cam] = ""

            # Define lambda functions
            toggle_cam_func = lambda x = cam: self.toggle_camera(x)
            settings_choose = lambda x = cam: self.get_file(x)
            settings_load = lambda x = cam: self.load_settings(x)

            self.dropdown_camera[cam] = ttk.Combobox(self.window_camera,
                state="readonly",
                justify=tk.CENTER,
                width=16,
                values=self.working_cams)
            self.dropdown_camera[cam].current(cam)
            self.button_open_camera[cam] = tk.Button(self.window_camera, 
                text=self.labels["t_cam_open"],
                width=15,
                command = toggle_cam_func) 
            self.button_settingsname[cam] = tk.Button(self.window_camera, 
                text=self.labels["t_settings_choose"][0], 
                width=15,
                command = settings_choose)
            self.button_loadsettings[cam] = tk.Button(self.window_camera, 
                text=self.labels["t_settings_load"], 
                width=15,
                command = settings_load)

            self.dropdown_camera[cam].grid_configure(row=1, column=cam, pady=(7,0), sticky="e")
            self.button_open_camera[cam].grid(row=2, column=cam, sticky="e")
            self.button_settingsname[cam].grid(row=3, column=cam, sticky="e")
            self.button_loadsettings[cam].grid(row=4, column=cam, sticky="e")
            self.dropdown_camera[cam].config(values=self.working_cams)

            # Bindings
            lambda_settings_enter = lambda function, x = cam: utils.hover(
                button=self.button_settingsname[x], 
                enter=True, 
                message=self.settings_path_short[x]
                )
            lambda_settings_leave = lambda function, x = cam: utils.hover(
                button=self.button_settingsname[x], 
                enter=False, 
                message=self.labels["t_settings_choose_current"][x]
                )

            self.button_settingsname[cam].bind(
                "<Enter>", 
                lambda_settings_enter
            )
            self.button_settingsname[cam].bind(
                "<Leave>", 
                lambda_settings_leave
            )

            
        for widgets in self.window_camera.winfo_children():
            widgets.grid_configure(padx=self.pad, pady=(2))
        self.button_preview.grid(row=0, column=0, pady=(20,20), columnspan=self.cam_n)
        


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
        [self.available_cams, self.working_cams, self.non_working_cams] = self.list_ports()
        self.working_cams_original = self.working_cams.copy()
        # self.working_cams.insert(0, self.t_cam_choose)

    def toggle_camera(self, cam):
        if not self.cam_opened[cam]:
                self.cam_opened[cam] = True
                print(self.cam_opened[cam])
                self.dropdown_camera[cam].config(state="disabled")
                self.button_open_camera[cam].config(text=self.labels["t_cam_close"])
                self.cap[cam] = cv2.VideoCapture(cam)
                print(self.cap)
                print(self.cap[cam])
                # for widget in self.widgets_cam_enable:
                #     widget.configure(state='normal')
        elif self.cam_opened[cam]: 
            self.cam_opened[cam] = False
            self.dropdown_camera[cam].config(state="readonly")
            self.button_open_camera[cam].config(text=self.labels["t_cam_open"])
            self.cap[cam].release()
            cv2.destroyAllWindows()
            # for widget in self.widgets_cam_disable:
            #     widget.configure(state='disable')
        # else:
        #     messagebox.showinfo(title=None, message=self.t_cam_choose)
        #     return
        if any(self.cam_opened.values()):
            self.button_preview.configure(state='normal')
        else:
            self.button_preview.configure(state='disabled')

    def toggle_preview(self):
        """Toggles Preview Start/Stop state"""
        if self.preview_running == False: # otherwise it starts
            self.preview_running = True
            self.button_preview.config(text = self.labels["t_preview_stop"], bg="red")
            # self.button_start.config(state="disabled")
            print("Caps: ", self.cap)
            while self.preview_running:
                for cam in self.cap:
                    ret, frame = self.cap[cam].read() # Capture frame-by-frame
                    if ret == True:
                        cv2.imshow("Cam %d" % cam, frame)
                if self.check_cv_break(self.cam_opened.values()):
                    break
                # self.root.update() # Needed to process new events
                self.window_camera.update()
        
        if self.preview_running == True: # if the experiment is running, it stops
            cv2.destroyAllWindows() # Just needs any input, though it's not using it here...
            self.preview_running = False
            self.button_preview.config(text=self.labels["t_preview"], bg="green")
            # self.button_start.config(state="normal")
        
    def list_ports(self):
        """
        Test the ports and returns a tuple with the available ports and the ones that are working.
        """
        non_working_ports = []
        dev_port = 0
        working_ports = []
        available_ports = []
        while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
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
            dev_port +=1
        return available_ports,working_ports,non_working_ports

    def check_cv_break(self, cam_opened):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        elif not any(cam_opened):
            return True

    def get_file(self, cam):
        self.settings_path[cam] = tk.filedialog.askopenfilename(
            parent=self.window_camera,
            initialdir="/home/",
            title=self.t_settings_choose[0])
        tk.Tk().withdraw()
        if (len(self.settings_path[cam]) - 20 <= 0):
            cutoff = 0
        else: 
            cutoff = len(self.settings_path[cam]) - 20
        self.settings_path_short[cam] = (self.settings_path[cam][:cutoff] and '..') + self.settings_path[cam][cutoff:] 
        self.t_settings_choose_current[cam] = self.t_settings_choose[1]
        self.button_settingsname[cam].config(text=self.t_settings_choose_current[cam])
        self.button_loadsettings[cam].configure(state='normal')

    def load_settings(self, cam):
        self.settings[cam] = toml.load(self.settings_path[cam])
        for key, value in self.settings[cam].items():
            cv_key = "cv2." + key
            print(cv_key, value)
            self.cap[cam].set(eval(cv_key), value)
            print(self.cap[cam].get(eval(cv_key)))

    def run(self):
        self.window_camera.mainloop()

