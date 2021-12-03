#!/usr/bin/python3.7

# Software
import os
import time
import datetime as dt
import tkinter as tk
from tkinter.filedialog import askdirectory
import pandas as pd

# Hardware
from picamera import PiCamera
from gpiozero import Button
from bme280 import BME280
import bh1745

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

bus = SMBus(1)
temp_sensor = BME280(i2c_dev=bus)
lux_sensor = bh1745.BH1745()
lux_sensor.setup()
lux_sensor.set_leds(0)

class BuxRecorder:
    def __init__(self):
        
        # Tkinter settings
        self.window = tk.Tk()
        self.window.title('Bux Recorder')
        self.window.geometry("350x230")
        self.window.resizable(0, 0)
        self.window.bind("<space>", self.toggle)
        self.label_1 = tk.Label(self.window, text='Choose folder:')
        self.label_1.grid(row=0, column=0, pady=(25,5), padx=10)
        
        self.path = ""
        self.dirname = tk.Button(self.window, text ='Select directory', command = self.get_dir)
        self.dirname.grid(row=0, column=1, pady=(25,5), padx=5)
        self.label_dir = tk.Label(self.window, text = self.path)
        self.label_dir.grid(row=1, column=1, pady=5, padx=5)
        
        self.label_2 = tk.Label(self.window, text = 'Record video:')
        self.label_2.grid(row=2, column=0, pady=5, padx=10)
        self.record = tk.IntVar()
        self.record.set(1)
        self.record_yes = tk.Radiobutton(self.window, text='Yes', value=1, variable=self.record)
        self.record_yes.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        self.record_no = tk.Radiobutton(self.window, text='No', value=-1, variable=self.record)
        self.record_no.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        
        self.start = tk.Button(self.window,
                               text='Start',
                               bg = "green",
                               command = self.toggle)
        self.start.grid(row=4, column=1, sticky="w", pady=10)
        
        # Camera settings
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)#(1920, 1080)#
        self.camera.framerate = 30#60
        self.camera.rotation = 180
        self.camera.color_effects = (128,128) # Black & white
        #self.camera.zoom = (0.15, 0.12, 0.68, 0.82)
        
        self.running = False
        self.temp_wait = 3
        self.start_dt = dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        self.start_time = time.time()
        self.data = pd.DataFrame(columns=['time','temperature','humidity','lux'])
        
        # Start GUI
        self.window.protocol("WM_DELETE_WINDOW", quit)
        tk.mainloop()
    
    def toggle(self, event=None):
        """When the Start/stop button is clicked, toggle and flip is invoked"""
        if self.start.config("text")[-1] == "Start":
            self.start.config(text = "Stop", bg="red")
            self.flip()
        else:
            self.start.config(text="Start", bg="green")
            self.flip()
            
    def flip(self):
        """Flips state and turns on/off the camera"""
        if self.running == False: # otherwise it starts
            self.running = True
            self.experimental_loop()
        
        elif self.running == True: # if the experiment is running, it stops
            self.close()
        
    def experimental_loop(self):
        """This is the main loop"""
        self.camera.start_preview(fullscreen=False, window=(100,20,640,480))
        print('Warming up...')
        time.sleep(1)
        if self.record.get() == 1:
            self.camera.start_recording(self.filename)
        try:
            print('Experiment running!')
            self.get_data()
            self.last = time.time()
            while self.running:
                self.window.update() # Always process new events
                self.now = time.time()
                if self.now - self.last >= self.temp_wait:
                    self.last = self.now
                    self.get_data()
        finally:
            pass
   
    def get_dir(self):
        """Ask user to input directory"""
        self.path = tk.filedialog.askdirectory(parent=self.window,
                                               initialdir="/home/pi/",
                                               title='Please select a directory')
        tk.Tk().withdraw()
        self.filename = os.path.join(self.path, '%s.h264'%(self.start_dt))
        self.csvname = os.path.join(self.path, '%s.csv'%(self.start_dt))
        self.label_dir.config(text=self.path)
        print(self.path)
    
    def get_data(self):
        temp = temp_sensor.get_temperature()
        humidity = temp_sensor.get_humidity()
        r, g, b, c = lux_sensor.get_rgbc_raw()
        self.data = self.data.append({'time': time.time() - self.start_time,
                                      'temperature': temp,
                                      'humidity': humidity,
                                      'lux': c}, ignore_index=True)
        print('{:7.1f}°C {:7.1f}% {:7.1f}'.format(temp,humidity,c))
    
    def close(self):
        self.running = False
        if self.record.get() == 1:
                self.camera.stop_recording()
        self.camera.stop_preview()
        self.data.to_csv(self.csvname)
        print("Experiment ended!")
                      
bux = BuxRecorder()