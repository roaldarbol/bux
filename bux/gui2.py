import time
import platform
import serial
import tkinter as tk
from tkinter import ttk
import cv2
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
        self.app = self.GUI()

    def GUI(self):
        """ Create the main UI window"""
        self.root = tk.Tk()
        self.root.title('Bux Recorder')
        self.root.geometry("550x350")
        self.root.resizable(0, 0)
        self.root.bind("<space>", self.toggle)
        self.root.protocol("WM_DELETE_root", quit)

        self.label_1 = tk.Label(self.root, text='Choose folder:')
        self.label_1.grid(row=0, column=0, pady=(25,5), padx=10)
        self.dirname = tk.Button(
            self.root, 
            text ='Select directory', 
            command = self.get_dir)
        self.dirname.grid(row=0, column=1, pady=(25,5), padx=5)
        self.path = ""
        self.label_dir = tk.Label(self.root, text = self.path)
        self.label_dir.grid(row=0, column=2, pady=(25,5), padx=5)  

        self.label_3 = tk.Label(self.root, text='Choose camera:')
        self.label_3.grid(row=2, column=0, pady=(25,5), padx=10)
        self.camera_dropdown = ttk.Combobox(self.root, values = self.working_cams)
        self.camera_dropdown.current(0)
        self.camera_dropdown.grid(
            row=2, 
            column=1, 
            sticky="w", 
            pady=(25,5))  

        self.preview_button = tk.Button(
            self.root, 
            text='Preview',
            command = self.preview_toggle)
        self.preview_button.grid(
            row=2, 
            column=2, 
            sticky="w", 
            pady=(25,5))  

        self.label_2 = tk.Label(self.root, text = 'Record video:')
        self.label_2.grid(row=4, column=0, pady=5, padx=10)
        self.record = tk.IntVar()
        self.record.set(1)
        self.record_yes = tk.Radiobutton(
            self.root, 
            text='Yes', 
            value=1, 
            variable=self.record)
        self.record_yes.grid(row=4, column=1, pady=5, padx=5, sticky="w")
        self.record_no = tk.Radiobutton(
            self.root, 
            text='No', 
            value=-1, 
            variable=self.record)
        self.record_no.grid(row=5, column=1, pady=5, padx=5, sticky="w")
        self.start_button = tk.Button(
            self.root, 
            text='Start',
            bg = "green",
            command = self.toggle)
        self.start_button.grid(
            row=6, 
            column=1, 
            sticky="w", 
            pady=10)      

    def preview_toggle(self):
        """Toggles Preview Start/Stop state"""
        if self.preview_running == False: # otherwise it starts
            self.preview_button.config(text = "Stop preview", bg="red")
            self.preview_running = True
            print('Preview running!')
            cap = cv2.VideoCapture(int(self.camera_dropdown.get()))
            
            while self.preview_running:
                ret, frame = cap.read() # Capture frame-by-frame
                if ret == True:
                    cv2.imshow('Frame',frame) # Display the resulting frame
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                self.root.update() # Needed to process new events
        
        if self.preview_running == True: # if the experiment is running, it stops
            cv2.destroyAllWindows()
            self.preview_button.config(text="Preview", bg="green")
            print("Preview ended")
            self.preview_running = False

    def toggle(self):
        """Toggles Start/Stop state"""
        if self.running == False: # otherwise it starts
            # self.ser = serial_connection.serial_connection("usb")
            # self.ser.connect_device()
            self.start_button.config(text = "Stop", bg="red")
            self.running = True
            self.experimental_loop()
        
        elif self.running == True: # if the experiment is running, it stops
            # bux.experiment.close()
            cv2.destroyAllWindows()
            self.start_button.config(text="Start", bg="green")
            # self.ser.close()
            print("Serial disconnected")
            self.running = False
    
    def experimental_loop(self):
        """Initiates the experimental loop"""
        print('Experiment running!')
        cap = cv2.VideoCapture(0)
        # Create txt or csv file here

        while self.running:
            ret, frame = cap.read() # Capture frame-by-frame
            if ret == True:
                cv2.imshow('Frame',frame) # Display the resulting frame
            self.root.update() # Needed to process new events

    def get_dir(self):
        """Ask user to input directory"""
        self.path = tk.filedialog.askdirectory(
            parent=self.root,
            initialdir="/home/",
            title='Please select a directory')
        tk.Tk().withdraw()
        self.label_dir.config(text=self.path)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = bux_recorder()
    app.run()