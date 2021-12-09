import time
import platform
import serial
import tkinter as tk
from bux.experiment import task
# import bux.test
import bux.utils
from bux.serial_connection import serial_connection

raspberry_pi = bux.utils.is_raspberrypi()
if raspberry_pi == False:
    print("You're not on a Raspberry Pi")

# This needs to go elsewhere
ser = serial_connection.device("usb")
if ser == None:
    print("Serial connection not established.")
 
# Functions
class bux_recorder():
    def __init__(self):
        self.running = False
        self.app = self.GUI()

    def GUI(self):
        """ Create the main UI window"""
        self.root = tk.Tk()
        self.root.title('Bux Recorder')
        self.root.geometry("350x230")
        self.root.resizable(0, 0)
        self.root.bind("<space>", self.toggle)
        self.root.protocol("WM_DELETE_root", quit)

        self.label_1 = tk.Label(self.root, text='Choose folder:')
        self.label_1.grid(row=0, column=0, pady=(25,5), padx=10)
        self.path = ""
        self.label_dir = tk.Label(self.root, text = self.path)
        self.label_dir.grid(row=1, column=1, pady=5, padx=5)
        self.dirname = tk.Button(
            self.root, 
            text ='Select directory', 
            command = self.get_dir)
        self.dirname.grid(row=0, column=1, pady=(25,5), padx=5)
        self.label_2 = tk.Label(self.root, text = 'Record video:')
        self.label_2.grid(row=2, column=0, pady=5, padx=10)

        self.record = tk.IntVar()
        self.record.set(1)
        self.record_yes = tk.Radiobutton(
            self.root, 
            text='Yes', 
            value=1, 
            variable=self.record)
        self.record_yes.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        self.record_no = tk.Radiobutton(
            self.root, 
            text='No', 
            value=-1, 
            variable=self.record)
        self.record_no.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        self.start_button = tk.Button(
            self.root, 
            text='Start',
            bg = "green",
            command = self.toggle)
        self.start_button.grid(
            row=4, 
            column=1, 
            sticky="w", 
            pady=10)        

    def toggle(self):
        """Toggles Start/Stop state"""
        if self.running == False: # otherwise it starts
            self.start_button.config(text = "Stop", bg="red")
            self.running = True
            self.experimental_loop()
        
        elif self.running == True: # if the experiment is running, it stops
            # bux.experiment.close()
            self.start_button.config(text="Start", bg="green")
            self.running = False
    
    def experimental_loop(self):
        """Initiates the experimental loop"""
        print('Experiment running!')
        # bux.test.open_stream()
        while self.running:
            task()
            # read_serial()
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