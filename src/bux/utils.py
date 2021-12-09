import os
import time
import csv
import serial
import tkinter as tk
from tkinter.filedialog import askdirectory
from serial.tools import list_ports

# From https://raspberrypi.stackexchange.com/a/118473
def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False


    start_dt = 5
    filename = os.path.join(path, '%s.h264'%(start_dt))
    csvname = os.path.join(path, '%s.csv'%(start_dt))
    print(path)