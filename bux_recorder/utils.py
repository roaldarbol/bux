import os
import platform
import time
import csv
import serial
import cv2
import tkinter as tk
from tkinter.filedialog import askdirectory
from serial.tools import list_ports

# From https://raspberrypi.stackexchange.com/a/118473
def is_raspberrypi():
    try:
        with io.open("/sys/firmware/devicetree/base/model", "r") as m:
            if "raspberry pi" in m.read().lower():
                return m
    except Exception:
        pass
    return False


def get_platform():
    return platform.system()


def get_gui_coordinates(root, w, h):
    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    return (w, h, x, y)


def handle_focus_in(button):
    full_name_entry.delete(0, tk.END)
    full_name_entry.config(fg="black")


def handle_focus_out(button):
    full_name_entry.delete(0, tk.END)
    full_name_entry.config(fg="grey")
    full_name_entry.insert(0, "Example: Joe Bloggs")


def hover(button, enter, message):
    if message == "":
        return
    else:
        button.configure(text=message)


def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while (
        len(non_working_ports) < 6
    ):  # if there are more than 5 non working ports stop the testing.
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            # print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                # print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                # print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port += 1
    return available_ports, working_ports, non_working_ports
