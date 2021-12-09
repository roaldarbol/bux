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

        # Main Window
        self.window = tk.Tk()
        self.window.title('Bux Recorder')
        self.window.geometry("350x230")
        self.window.resizable(0, 0)
        self.window.bind("<space>", self.toggle)
        self.window.protocol("WM_DELETE_WINDOW", quit)

        self.label_1 = tk.Label(self.window, text='Choose folder:')
        self.label_1.grid(row=0, column=0, pady=(25,5), padx=10)
        self.path = ""
        self.label_dir = tk.Label(self.window, text = self.path)
        self.label_dir.grid(row=1, column=1, pady=5, padx=5)
        self.dirname = tk.Button(
            self.window, 
            text ='Select directory', 
            command = self.get_dir)
        self.dirname.grid(row=0, column=1, pady=(25,5), padx=5)
        self.label_2 = tk.Label(self.window, text = 'Record video:')
        self.label_2.grid(row=2, column=0, pady=5, padx=10)

        self.record = tk.IntVar()
        self.record.set(1)
        self.record_yes = tk.Radiobutton(self.window, text='Yes', value=1, variable=self.record)
        self.record_yes.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        self.record_no = tk.Radiobutton(self.window, text='No', value=-1, variable=self.record)
        self.record_no.grid(row=3, column=1, pady=5, padx=5, sticky="w")

        self.start_button = tk.Button(
            self.window, 
            text='Start',
            bg = "green",
            command = self.toggle)
        self.start_button.grid(
            row=4, 
            column=1, 
            sticky="w", 
            pady=10)

        self.window.mainloop()

    def toggle(self):
        """Toggles state"""
        if self.running == False: # otherwise it starts
            self.start_button.config(text = "Stop", bg="red")
            self.running = True
            self.start_experiment()
        
        elif self.running == True: # if the experiment is running, it stops
            # bux.experiment.close()
            self.start_button.config(text="Start", bg="green")
            self.running = False
    
    def start_experiment(self):
        print('Experiment running!')
        last = time.time()
        # bux.test.open_stream()
        while self.running:
            task()
            # get_serial()
            self.window.update() # Always process new events

    def get_dir(self):
        """Ask user to input directory"""
        self.path = tk.filedialog.askdirectory(
            parent=self.window,
            initialdir="/home/",
            title='Please select a directory')
        tk.Tk().withdraw()
        self.label_dir.config(text=self.path)
    # ----

    