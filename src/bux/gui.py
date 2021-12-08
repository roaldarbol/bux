import time
import platform
import tkinter as tk
from bux.example import task
from bux.utils import is_raspberrypi

running = False
raspberry_pi = is_raspberrypi()
print(raspberry_pi)
 
# Functions

def toggle():
    """Toggles state"""
    global running

    if running == False: # otherwise it starts
        start_button.config(text = "Stop", bg="red")
        running = True
        start_experiment()
    
    elif running == True: # if the experiment is running, it stops
        start_button.config(text="Start", bg="green")
        running = False

def start_experiment():
    try:
        print('Experiment running!')
        last = time.time()
        while running:
            task()
            window.update() # Always process new events
            
    finally:
        pass

# ----

# Main Window
window = tk.Tk()
window.title('Bux Recorder')
window.geometry("350x230")
window.resizable(0, 0)
window.protocol("WM_DELETE_WINDOW", quit)
label_1 = tk.Label(
    window, 
    text='Choose folder:')
label_1.grid(
    row=0, 
    column=0, 
    pady=(25,5), 
    padx=10)
start_button = tk.Button(
    window, 
    text='Start',
    bg = "green",
    command = toggle)
start_button.grid(
    row=0, 
    column=1, 
    pady=(25,5), 
    padx=5
    )

def bux():
    window.mainloop()

    