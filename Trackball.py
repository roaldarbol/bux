#!/usr/bin/env python3

import mouse
import math
import time
import numpy as np
import pandas as pd
import tkinter as tk
import tkinter.filedialog
import platform

# Not currently used, but will hopefully
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import animation
from matplotlib import pyplot as plt


class Trackball:

	def __init__(self):

		# Initial values
		self.platform = platform.system()
		self.pos_init = np.array([[800,400]])
		self.hz = 130 # Cursor polling rate
		self.moves = np.empty([0,5])
		self.new_pos = np.zeros(2)
		self.calibration = 100
		self.phi = 0
		self.state = False

	    # Create the root window
		self.root = tk.Tk()
		self.root.title('Trackball Recorder')
		self.root.geometry("350x230")
		self.root.resizable(0, 0)
		self.root.bind("<space>", self.switch) # Checks for space press to switch self.state
		self.frame = tk.Frame(self.root)
		self.frame.pack_propagate(0) # Don't allow widgets to determine size
		self.frame.pack()

		# Make the labels, buttons, etc. to populate the GUI
		self.label_1 = tk.Label(self.frame, text='Choose folder:')
		self.label_1.grid(row=0, column=0, pady=(25,5), padx=5)
		self.dirname = tk.Button(self.frame, text ='Select directory', command = self.choose_dir)
		self.dirname.grid(row=0, column=1, pady=(25,5), padx=5)
		self.animal_ent = tk.Spinbox(self.frame, from_=1, to=100, width=12)
		self.animal_ent.grid(row=1, column=1, pady=5, padx=5)
		self.label_2 = tk.Label(self.frame, text = 'Animal ID:')
		self.label_2.grid(row=1, column=0, pady=5, padx=5)
		
		self.selected = tk.StringVar(None, "mouse")
		self.mouse = tk.Radiobutton(self.frame, text='Mouse', value='mouse', variable=self.selected)
		self.mouse.grid(row=2, column=1, pady=5, padx=5, sticky="w")
		self.of_sensor = tk.Radiobutton(self.frame, text='OF Sensors', value='opticflow', variable=self.selected)
		self.of_sensor.grid(row=3, column=1, pady=5, padx=5, sticky="w")
		self.label_3 = tk.Label(self.frame, text = 'Sensor type:')
		self.label_3.grid(row=2, column=0, pady=5, padx=5)
		self.start = tk.Button(self.frame, text='Start (stop with SPACE)', command = self.experiment_loop)
		self.start.grid(row=4, column=1, sticky="w", pady=10)

	    # Enter the main loop
		tkinter.mainloop()

	def experiment_loop(self):
		if self.selected.get() == 'mouse':
			self.mouse_exp()
		elif self.selected.get() == 'opticflow':
			pass


	def switch(self, event):
		self.state = not self.state

	def choose_dir(self):
	   self.input = tk.filedialog.askdirectory(parent=self.root, initialdir="/",
	                                    title='Please select a directory')

	def output_csv(self):
		df = pd.DataFrame(self.moves, columns=('phi', 'dist', 'x', 'y', 'time'))
		df.to_csv(self.input + '/' + self.animal_id + '-%s.csv' % self.dt)


	def mouse_exp(self):
		self.dt = time.strftime("%Y%m%d-%H%M%S") # Date and time of the beginning of experiment
		self.t0 = time.time()
		self.animal_id = self.animal_ent.get()
		self.start['state'] = tk.DISABLED
		self.animal_ent['state'] = tk.DISABLED
		self.state = True

		try:
			while self.state == True:
				# Move cursor back
				self.root.update() # Always process new events
				mouse.move(self.pos_init[0,0], self.pos_init[0,1], absolute=True)

				# Sleep...
				#time.sleep(1/(2*self.hz))

				# Get cursor displacement
				self.update_data()
				
		finally:
			self.output_csv()
			self.start['state'] = tk.NORMAL
			self.animal_ent['state'] = tk.NORMAL

	def update_data(self):
		mousepos_abs = np.asarray(mouse.get_position())# np.array([mousepos.x, mousepos.y])
		mousepos_diff = np.subtract(mousepos_abs, self.pos_init)
		phi, dist = mousepos_diff[0]
		self.phi = self.phi + phi
		self.phi_ang = (self.phi/self.calibration)%(2*math.pi)
		self.pos_change = math.sin(self.phi_ang)*dist, math.cos(self.phi_ang)*dist
		self.new_pos = self.new_pos + self.pos_change
		curr_time = time.time() - self.t0
		mousepos_timed = np.array([self.phi_ang, dist, self.new_pos[0], self.new_pos[1], curr_time])
		self.moves = np.append(self.moves, [mousepos_timed], axis=0)
		return self.moves

gui = Trackball()