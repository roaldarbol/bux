import os
import time
import datetime as dt
import platform
import serial
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import toml
import cv2

# From the bux package
# from bux.experiment import task
# import bux.test
import bux.utils
import bux.record_video
# import bux.serial_connection as serial_connection

raspberry_pi = bux.utils.is_raspberrypi()
if raspberry_pi == False:
    print("You're not on a Raspberry Pi")



# Functions
class bux_recorder():
    def __init__(self):
        self.running = False
        self.preview_running = False
        [self.available_cams, self.working_cams, self.non_working_cams] = bux.utils.list_ports()
        self.working_cams_original = self.working_cams.copy()
        self.working_cams.insert(0, "Choose camera")
        self.cam_opened = False
        self.path = ""
        self.settings_path = "/Users/roaldarbol/MEGA/Documents/sussex/projects/buxr/video_settings.toml"
        self.app = self.GUI()

    def get_gui_coordinates(self, w, h):
        # get screen width and height
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        return(w,h,x,y)

    def GUI(self):
        """ Create the main UI window"""
        self.root = tk.Tk()
        self.root.title('Bux Recorder')
        self.gui_coordinates = self.get_gui_coordinates(450, 300)
        self.root.geometry('%dx%d+%d+%d' % self.gui_coordinates)
        self.root.resizable(0, 0)
        # self.root.bind("<space>", self.toggle) # Removed space access to Start Experiment
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.columnconfigure(0, minsize=250)
        self.root.columnconfigure(1, minsize=250)

        """Create GUI Elements"""
        self.button_dirname = tk.Button(self.root, 
            text ='Select directory', 
            width=15,
            command = self.get_dir)
        self.label_dirname = tk.Label(self.root, 
            text = '')
        self.dropdown_camera = ttk.Combobox(self.root,
            state="readonly",
            justify=tk.CENTER,
            width=16,
            values = self.working_cams)
        self.dropdown_camera.current(0)
        self.button_open_camera = tk.Button(self.root, 
            text='Initiate camera',
            width=15,
            command = lambda: self.open_camera(self.dropdown_camera.get())) 
        self.button_settingsname = tk.Button(self.root, 
            text ='Select settings file', 
            width=15,
            command = self.get_file)
        self.label_settings = tk.Label(self.root, 
            text = self.settings_path) 
        self.button_loadsettings = tk.Button(self.root, 
            text ='Load settings', 
            width=15,
            command = self.load_settings)
        self.button_preview = tk.Button(self.root, 
            text='Preview',
            width=15,
            command = self.preview_toggle)
        self.button_start = tk.Button(self.root, 
            text='Start Recording',
            width=15,
            bg = "green",
            command = self.toggle)

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

        for widget in self.widgets_cam_disable:
                widget.configure(state='disable')

        """Position elements into grid"""
        # First we assign padding to all widgets
        for widgets in self.root.winfo_children():
            widgets.grid_configure(padx=5, pady=(5,5))
        
        # Then customise placement
        self.button_dirname.grid_configure(row=0, column=0, pady=(30,0))
        self.label_dirname.grid_configure(row=0, column=1, sticky = "w", pady=(30,0))
        self.dropdown_camera.grid_configure(row=1, column=0, pady=(7,0))  
        self.button_open_camera.grid(row=2, column=0) 
        self.button_settingsname.grid(row=3, column=0)
        self.label_settings.grid(row=3, column=1, sticky = "w")
        self.button_loadsettings.grid(row=4, column=0)
        self.button_preview.grid(row=5, column=0) 
        self.button_start.grid(row=6, column=0)
    
    def open_camera(self, n):
        if not self.cam_opened:
            print(n.isnumeric())
            if not n.isnumeric():
                messagebox.showinfo(title=None, message="Choose a camera")
                return
            else:
                self.cam_opened = True
                self.button_open_camera.config(text="Close camera")
                self.cap = cv2.VideoCapture(int(n))
                for widget in self.widgets_cam_enable:
                    widget.configure(state='normal')
        elif self.cam_opened: 
            self.cam_opened = False
            self.button_open_camera.config(text="Initiate camera")
            self.cap.release()
            cv2.destroyAllWindows()
            for widget in self.widgets_cam_disable:
                widget.configure(state='disable')

    def read_frame(self, cam, out):
        ret, frame = cam.read() # Capture frame-by-frame
        if ret == True:
            cv2.imshow('Frame',frame) # Display the resulting frame
        if out:
            out.write(frame)
    
    def check_cv_break(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        elif not self.cam_opened:
            return True

    def preview_toggle(self):
        """Toggles Preview Start/Stop state"""
        if self.preview_running == False: # otherwise it starts
            self.preview_running = True
            self.button_preview.config(text = "Stop preview", bg="red")
            self.button_start.config(state="disabled")
            print('Preview running')
            
            while self.preview_running:
                self.read_frame(self.cap, out = False)
                if self.check_cv_break():
                    break
                self.root.update() # Needed to process new events
        
        if self.preview_running == True: # if the experiment is running, it stops
            cv2.destroyAllWindows() # Just needs any input, though it's not using it here...
            self.preview_running = False
            self.button_preview.config(text="Preview", bg="green")
            self.button_start.config(state="normal")
            print("Preview ended")

    def toggle(self):
        """Toggles Start/Stop state"""
        if self.running == False: # otherwise it starts
            # self.ser = serial_connection.serial_connection("usb")
            # self.ser.connect_device()
            self.running = True
            self.button_start.config(text = "Stop Recording", bg="red")
            self.button_preview.config(state="disabled")
            print('Recording running')
            self.experimental_loop()
            self.out.release()
            self.root.update()
        
        if self.running == True: # if the experiment is running, it stops
            # bux.experiment.close()
            cv2.destroyAllWindows()
            self.button_start.config(text="Start Recording", bg="green")
            self.button_preview.config(state="disabled")
            # self.ser.close()
            # print("Serial disconnected")
            self.running = False
            print('Recording ended')
    
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
            self.read_frame(self.cap, out = self.out)
            if self.check_cv_break():
                break
            self.root.update() # Needed to process new events

    def get_dir(self):
        """Ask user to input directory"""
        self.path = tk.filedialog.askdirectory(
            parent=self.root,
            initialdir="/home/",
            title='Please select a directory')
        tk.Tk().withdraw()
        if (len(self.path) - 25 <= 0):
            cutoff = 0
        else: 
            cutoff = len(self.path) - 25
        self.short_path = (self.path[:cutoff] and '..') + self.path[cutoff:] 
        self.label_dirname.config(text=self.short_path)

    def get_file(self):
        self.settings_path = tk.filedialog.askopenfilename(
            parent=self.root,
            initialdir="/home/",
            title='Please select a settings file')
        tk.Tk().withdraw()
        if (len(self.settings_path) - 25 <= 0):
            cutoff = 0
        else: 
            cutoff = len(self.settings_path) - 25
        self.short_settings_path = (self.settings_path[:cutoff] and '..') + self.settings_path[cutoff:] 
        self.label_settings.config(text=self.short_settings_path)
        self.button_loadsettings.configure(state='normal')

    def load_settings(self):
        self.settings = toml.load(self.settings_path)
        for key, value in self.settings.items():
            cv_key = "cv2." + key
            print(cv_key, value)
            self.cap.set(eval(cv_key), value)
            print(self.cap.get(eval(cv_key)))
    
    def close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit Bux?"):
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