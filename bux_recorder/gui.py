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

# From the bux package
import bux_recorder.utils as utils
import bux_recorder.video as video
import bux_recorder.serial_connection as serial_connection

raspberry_pi = utils.is_raspberrypi()
if raspberry_pi == False:
    print("You're not on a Raspberry Pi")



# Functions
class bux_recorder():
    def __init__(self):
        self.t_dir_choose = ["Select directory", "Directory chosen"]
        self.t_dir_choose_current = self.t_dir_choose[0]
        self.t_cam_choose = "Choose camera"
        self.t_cam_open = "Open camera"
        self.t_cam_close = "Close camera"
        self.t_serial_choose = "Choose serial"
        self.t_serial_open = "Open serial"
        self.t_serial_close = "Close serial"
        self.t_serial_send = "Send to serial"
        self.t_script_choose = "Choose script"
        self.t_settings_choose = ["Select settings", "Settings selected"]
        self.t_settings_choose_current = self.t_settings_choose[0]
        self.t_settings_load = "Load settings"
        self.t_preview = "Preview"
        self.t_preview_stop = "Stop preview"
        self.t_start = "Start recording"
        self.t_stop = "Stop recording"
        self.t_quit = "Do you want to quit Bux?"

        self.running = False
        self.preview_running = False
        [self.available_cams, self.working_cams, self.non_working_cams] = utils.list_ports()
        self.working_serial = []
        for port in list(list_ports.comports()):
            self.working_serial.append(port.device)
        self.working_serial_original = self.working_serial.copy()
        self.working_serial.insert(0, self.t_serial_choose)
        self.working_cams_original = self.working_cams.copy()
        self.working_cams.insert(0, self.t_cam_choose)
        self.cam_opened = False
        self.serial_opened = False
        self.path = ""
        self.path_short = ""
        self.settings_path = "/Users/roaldarbol/MEGA/Documents/sussex/projects/bux-recorder/video_settings.toml"
        self.settings_path_short = ""
        self.app = self.GUI()

    def GUI(self):
        """ Create the main UI window"""
        self.root = tk.Tk()
        self.root.title('Bux Recorder')
        self.w, self.h = 450, 500
        self.gui_coordinates = utils.get_gui_coordinates(self.root, self.w, self.h)
        self.pad = 10
        self.col_width = (self.w / 2)

        self.root.geometry('%dx%d+%d+%d' % self.gui_coordinates)
        self.root.resizable(0, 0)
        # self.root.bind("<space>", self.toggle) # Removed space access to Start Experiment
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.columnconfigure(0, minsize=self.col_width)
        self.root.columnconfigure(1, minsize=self.col_width)

        """Create GUI Elements"""
        # === TOP PANEL === #
        self.label_title = tk.Label(self.root,
            text="BUX",
            justify=tk.CENTER,
            font=("Avenir", 44)
            # height=70
        )

        # === LEFT PANEL === #
        self.dropdown_camera = ttk.Combobox(self.root,
            state="readonly",
            justify=tk.CENTER,
            width=16,
            values = self.working_cams)
        self.dropdown_camera.current(0)
        self.button_open_camera = tk.Button(self.root, 
            text=self.t_cam_open,
            width=15,
            command = lambda: self.toggle_camera(self.dropdown_camera.get())) 
        self.button_settingsname = tk.Button(self.root, 
            text=self.t_settings_choose[0], 
            width=15,
            command = self.get_file)
        self.button_loadsettings = tk.Button(self.root, 
            text=self.t_settings_load, 
            width=15,
            command = self.load_settings)
        self.button_preview = tk.Button(self.root, 
            text=self.t_preview,
            width=15,
            command = self.preview_toggle)


        # === RIGHT PANEL === #
        self.dropdown_serial = ttk.Combobox(self.root,
            state="readonly",
            justify=tk.CENTER,
            width=16,
            values = self.working_serial)
        self.dropdown_serial.current(0)
        self.button_open_serial = tk.Button(self.root, 
            text=self.t_serial_open,
            width=15,
            command= lambda: self.toggle_serial(self.dropdown_serial.get())
        )
        self.dropdown_scripts = ttk.Combobox(self.root,
            state="readonly",
            justify=tk.CENTER,
            width=16,
            values=None
            )
        self.text_command = tk.Entry(self.root,
            width=17
        ) # Include example text: https://stackoverflow.com/questions/51781651/showing-a-greyed-out-default-text-in-a-tk-entry
        self.button_send_serial = tk.Button(self.root, 
            text=self.t_serial_send,
            width=15,
            command= lambda: self.send_serial(self.dropdown_scripts.get(), self.text_command.get())
        )
        
        # === BOTTOM PANEL === #
        self.button_dirname = tk.Button(self.root, 
            text = self.t_dir_choose[0], 
            width=15,
            command = self.get_dir)
        self.button_start = tk.Button(self.root, 
            text=self.t_start,
            width=15,
            bg = "green",
            command = self.toggle)
        self.sysinfo = tk.Label(self.root,
            text="OS: " + utils.get_platform(),
            font=('TkDefaultFont', 8)
        )

        """Disable camera buttons"""
        self.widgets_cam_enable = [
            self.button_preview,
            self.button_start
        ]
        self.widgets_cam_disable = [
            self.button_loadsettings,
            self.button_preview,
            self.button_start
        ]

        self.widgets_serial = [
            self.text_command,
            self.dropdown_scripts,
            self.button_send_serial
        ]

        for widget in self.widgets_cam_disable + self.widgets_serial:
                widget.configure(state='disable')

        """Position elements into grid"""
        # First we assign padding to all widgets
        for widgets in self.root.winfo_children():
            widgets.grid_configure(padx=5, pady=(5,5))
        
        # Then customise placement
        self.label_title.grid(row=0, column=0, columnspan=2, padx=(50,50), pady=(30,30))
        self.dropdown_camera.grid_configure(row=1, column=0, pady=(7,0))
        self.button_open_camera.grid(row=2, column=0)
        self.button_settingsname.grid(row=3, column=0)
        self.button_loadsettings.grid(row=4, column=0)
        self.button_preview.grid(row=5, column=0)
        
        self.dropdown_serial.grid(row=1, column=1, pady=(7,0))
        self.button_open_serial.grid(row=2, column=1) 
        self.dropdown_scripts.grid(row=3, column=1)
        self.text_command.grid(row=4, column=1)
        self.button_send_serial.grid(row=5, column=1)
        # self.dropdown_functions.grid(row=6, column=6)

        self.button_dirname.grid_configure(row=6, column=0, pady=(50,0), columnspan = 2)
        self.button_start.grid(row=7, column=0, columnspan = 2)
        self.sysinfo.grid(row=10, column=0, sticky="sw", padx=25, pady=25)
        
        

        """Bindings"""
        self.button_dirname.bind(
            "<Enter>", 
            lambda function: (
                self.hover(
                    button=self.button_dirname, 
                    enter=True, 
                    message=self.path_short
                )
            )
        )
        self.button_dirname.bind(
            "<Leave>", 
            lambda function: (
                self.hover(
                    button=self.button_dirname, 
                    enter=False, 
                    message=self.t_dir_choose_current
                )
            )
        )
        self.button_settingsname.bind(
            "<Enter>", 
            lambda function: (
                self.hover(
                    button=self.button_settingsname, 
                    enter=True, 
                    message=self.settings_path_short
                )
            )
        )
        self.button_settingsname.bind(
            "<Leave>", 
            lambda function: (
                self.hover(
                    button=self.button_settingsname, 
                    enter=False, 
                    message=self.t_settings_choose_current
                )
            )
        )
    

    def hover(self, button, enter, message):
        if message == "":
            return
        else:
            button.configure(text=message)
        
    
    def toggle_serial(self, serial):
        if not self.serial_opened:
            if serial not in self.working_serial_original:
                messagebox.showinfo(title=None, message=self.t_serial_choose)
                return
            else:
                self.ser = MailMan(serial)
                self.serial_scripts_raw = serial_connection.get_scripts(self.ser)
                self.serial_scripts_py = self.serial_scripts_raw.split("'")[1::2]
                self.serial_scripts_py.insert(0, self.t_script_choose)
                self.serial_opened = True
                self.dropdown_serial.config(state="disabled")
                self.button_open_serial.config(text=self.t_serial_close)
                self.dropdown_scripts.config(values=self.serial_scripts_py)
                self.dropdown_scripts.current(0)
                for widget in self.widgets_serial:
                        widget.configure(state='normal')
        elif self.serial_opened:
            self.serial_opened = False
            self.dropdown_serial.config(state="readonly")
            self.button_open_serial.config(text=self.t_serial_open)
            self.ser.close()
            for widget in self.widgets_serial:
                    widget.configure(state='disable')

    def send_serial(self, script, message):
        message = script.strip("py") + message
        print(message)
        self.ser.send(message)
        print(self.ser.receive())
    
    def toggle_camera(self, n):
        if not self.cam_opened:
            if not n.isnumeric():
                self.dropdown_camera.config(state="readonly")
                messagebox.showinfo(title=None, message=self.t_cam_choose)
                return
            else:
                self.cam_opened = True
                self.dropdown_camera.config(state="disabled")
                self.button_open_camera.config(text=self.t_cam_close)
                self.cap = cv2.VideoCapture(int(n))
                for widget in self.widgets_cam_enable:
                    widget.configure(state='normal')
        elif self.cam_opened: 
            self.cam_opened = False
            self.dropdown_camera.config(state="readonly")
            self.button_open_camera.config(text=self.t_cam_open)
            self.cap.release()
            cv2.destroyAllWindows()
            for widget in self.widgets_cam_disable:
                widget.configure(state='disable')

    def preview_toggle(self):
        """Toggles Preview Start/Stop state"""
        if self.preview_running == False: # otherwise it starts
            self.preview_running = True
            self.button_preview.config(text = self.t_preview_stop, bg="red")
            self.button_start.config(state="disabled")
            
            while self.preview_running:
                video.read_frame(self.cap, out = False)
                if video.check_cv_break(self.cam_opened):
                    break
                self.root.update() # Needed to process new events
        
        if self.preview_running == True: # if the experiment is running, it stops
            cv2.destroyAllWindows() # Just needs any input, though it's not using it here...
            self.preview_running = False
            self.button_preview.config(text=self.t_preview, bg="green")
            self.button_start.config(state="normal")

    def toggle(self):
        """Toggles Start/Stop state"""
        if self.running == False: # otherwise it starts
            # self.ser = serial_connection.serial_connection("usb")
            # self.ser.connect_device()
            self.running = True
            self.button_start.config(text = self.t_stop, bg="red")
            self.button_preview.config(state="disabled")
            self.experimental_loop()
            self.out.release()
            self.root.update()
        
        if self.running == True: # if the experiment is running, it stops
            # bux.experiment.close()
            cv2.destroyAllWindows()
            self.button_start.config(text=self.t_start, bg="green")
            self.button_preview.config(state="disabled")
            # self.ser.close()
            # print("Serial disconnected")
            self.running = False
    
    def experimental_loop(self):
        """Initiates the experimental loop"""
        self.start_dt = dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        # INSERT ERROR STUFF IF PATH DOESN'T EXIST
        self.videoname = os.path.join(self.path, '%s.mp4'%(self.start_dt))
        self.csvname = os.path.join(self.path, '%s.csv'%(self.start_dt))
        
        # Get the width and height of frame
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
        self.out = cv2.VideoWriter(self.videoname, fourcc, 30.0, (width, height))

        # Create txt or csv file here

        while self.running:
            video.read_frame(self.cap, out = self.out)
            if video.check_cv_break(self.cam_opened):
                break
            self.root.update() # Needed to process new events

    def get_dir(self):
        """Ask user to input directory"""
        self.path = tk.filedialog.askdirectory(
            parent=self.root,
            initialdir="/home/",
            title=self.t_dir_choose[0])
        tk.Tk().withdraw()
        if (len(self.path) - 20 <= 0):
            cutoff = 0
        else: 
            cutoff = len(self.path) - 20
        self.path_short = (self.path[:cutoff] and '..') + self.path[cutoff:] 
        self.t_dir_choose_current = self.t_dir_choose[1]
        self.button_dirname.config(text=self.t_dir_choose_current)
        
    def get_file(self):
        self.settings_path = tk.filedialog.askopenfilename(
            parent=self.root,
            initialdir="/home/",
            title=self.t_settings_choose[0])
        tk.Tk().withdraw()
        if (len(self.settings_path) - 25 <= 0):
            cutoff = 0
        else: 
            cutoff = len(self.settings_path) - 25
        self.settings_path_short = (self.settings_path[:cutoff] and '..') + self.settings_path[cutoff:] 
        self.t_settings_choose_current = self.t_settings_choose[1]
        self.button_settingsname.config(text=self.t_settings_choose_current)
        self.button_loadsettings.configure(state='normal')

    def load_settings(self):
        self.settings = toml.load(self.settings_path)
        for key, value in self.settings.items():
            cv_key = "cv2." + key
            print(cv_key, value)
            self.cap.set(eval(cv_key), value)
            print(self.cap.get(eval(cv_key)))
    
    def close(self):
        if messagebox.askokcancel("Quit", self.t_quit):
            if self.cam_opened:
                self.cam_opened = False
                self.cap.release()
                cv2.destroyAllWindows()
                exit()
            else:
                exit()
        

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = bux_recorder()
    app.run()