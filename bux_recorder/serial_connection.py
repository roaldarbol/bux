import time
import serial
from serial.tools import list_ports

def get_scripts(serial):
    serial.send("os.listdir()")
    return serial.receive()
