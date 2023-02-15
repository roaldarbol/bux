import time
import select
import belay
import tkinter as tk
from tkinter import ttk

from bux_recorder.frontend.label_text import create_labels
import bux_recorder.backend.utils as utils


class SerialWindow:
    def __init__(self, labels, coordinates, toplevel=None):
        self.labels = labels
        if toplevel is None:
            self.window_serial = tk.Tk()
        else:
            self.window_serial = tk.Toplevel(toplevel)

        # sets the title of the
        # Toplevel widget
        self.working_serial = [self.labels["t_serial_choose"]]
        self.update_serial()
        self.colwidth = 180
        self.pad = 10
        self.ser_n = len(self.working_serial)
        self.w, self.h = self.colwidth * self.ser_n + self.pad * 2 * self.ser_n, 240
        self.x, self.y = (
            coordinates[2] + coordinates[0] + 10,
            coordinates[3] + 250 + self.pad,
        )
        self.window_coord = self.w, self.h, self.x, self.y
        self.window_serial.geometry("%dx%d+%d+%d" % self.window_coord)
        self.window_serial.title("Serial devices")

        # --- CREATE WIDGET DICTS --- #
        self.pyb = {}
        self.poll = {}
        self.serial_scripts_raw = {}
        self.serial_scripts_py = {}
        self.serial_opened = {}
        self.serial_running = {}
        self.dropdown_serial = {}
        self.button_open_serial = {}
        self.dropdown_scripts = {}
        self.text_command = {}
        self.button_send_serial = {}
        self.button_send_interrupt = {}
        self.TERMINATOR = "\r".encode("utf8")

        # --- CREATE WIDGETS FOR EACH SERIAL DEVICE --- #
        for ser in self.working_serial:
            ser_n = self.working_serial.index(ser)
            # print("here", ser_n, type(ser_n))
            self.serial_opened[ser_n] = False
            self.window_serial.columnconfigure(ser_n, minsize=self.colwidth)

            # Define lambda functions
            # toggle_cam_func = lambda x = cam: self.toggle_camera(x)
            lambda_toggle_serial = lambda x=ser_n: (self.toggle_serial(ser_n))
            lambda_send_serial = lambda x=ser_n: (
                self.send_serial(
                    x,
                    self.pyb[x],
                    self.dropdown_scripts[x].get(),
                    self.text_command[x].get(),
                )
            )
            lambda_send_interrupt = lambda x=ser_n: (self.send_interrupt(self.pyb[x]))

            self.dropdown_serial[ser_n] = ttk.Combobox(
                self.window_serial,
                state="readonly",
                justify=tk.CENTER,
                width=16,
                values=self.working_serial,
            )
            self.dropdown_serial[ser_n].current(ser_n)
            self.button_open_serial[ser_n] = tk.Button(
                self.window_serial,
                text=self.labels["t_serial_open"],
                width=15,
                command=lambda_toggle_serial,
            )
            self.dropdown_scripts[ser_n] = ttk.Combobox(
                self.window_serial,
                state="readonly",
                justify=tk.CENTER,
                width=16,
                values=None,
            )
            self.text_command[ser_n] = tk.Entry(
                self.window_serial, width=17
            )  # Include example text: https://stackoverflow.com/questions/51781651/showing-a-greyed-out-default-text-in-a-tk-entry
            self.button_send_serial[ser_n] = tk.Button(
                self.window_serial,
                text=self.labels["t_serial_send"],
                width=15,
                command=lambda_send_serial,
            )
            self.button_send_interrupt[ser_n] = tk.Button(
                self.window_serial,
                text=self.labels["t_serial_interrupt"],
                width=15,
                command=lambda_send_interrupt,
            )

            self.dropdown_serial[ser_n].grid(row=1, column=ser_n, pady=(20, 0))
            self.button_open_serial[ser_n].grid(row=2, column=ser_n)
            self.dropdown_scripts[ser_n].grid(row=3, column=ser_n)
            self.text_command[ser_n].grid(row=4, column=ser_n)
            self.button_send_serial[ser_n].grid(row=5, column=ser_n)
            self.button_send_interrupt[ser_n].grid(row=6, column=ser_n)

            # --- BINDINGS --- #

            for widgets in self.window_serial.winfo_children():
                widgets.grid_configure(padx=self.pad, pady=(2))

    def update_serial(self):
        self.working_serial = []
        # for port in list(list_ports.comports()):
        #     self.working_serial.append(port.device)
        self.working_serial_original = self.working_serial.copy()
        # self.working_serial.insert(0, self.labels["t_serial_choose"])
        # self.dropdown_serial.config(values=self.working_serial)

    def toggle_serial(self, serial):
        if not self.serial_opened[serial]:
            device = self.working_serial[serial]
            self.pyb[serial] = pyboard.Pyboard(device, 115200)
            self.serial_scripts_raw[serial] = self.get_scripts(self.pyb[serial])
            self.serial_scripts_py[serial] = self.serial_scripts_raw[serial].split("'")[
                1::2
            ]
            self.serial_scripts_py[serial].insert(0, self.labels["t_script_choose"])
            self.serial_opened[serial] = True
            self.serial_running[serial] = False
            self.dropdown_serial[serial].config(state="disabled")
            self.button_open_serial[serial].config(text=self.labels["t_serial_close"])
            self.dropdown_scripts[serial].config(values=self.serial_scripts_py[serial])
            self.dropdown_scripts[serial].current(0)
            # for widget in self.widgets_serial:
            #         widget.configure(state='normal')
        elif self.serial_opened[serial]:
            self.serial_opened[serial] = False
            self.dropdown_serial[serial].config(state="readonly")
            self.button_open_serial[serial].config(text=self.labels["t_serial_open"])
            self.pyb[serial].exit_raw_repl()
            self.pyb[serial].close()
            # for widget in self.widgets_serial:
            #         widget.configure(state='disable')

    def get_scripts(self, serial):
        self.send("import os; print(os.listdir())")
        return serial.receive()

    def send_serial(self, ser_n, serial, script, message):
        if not self.serial_running[ser_n]:
            message = script.strip("py") + message
            self.serial_running[ser_n] = not self.serial_running[ser_n]
            self.button_send_serial[ser_n].config(
                text=self.labels["t_serial_interrupt"]
            )
        else:
            message = "raise KeyboardInterrupt"
            self.serial_running[ser_n] = not self.serial_running[ser_n]
            self.button_send_serial[ser_n].config(text=self.labels["t_serial_send"])
        # print(message)
        serial.send(message)

    def send_interrupt(self, serial):
        serial.send("\x03")

    def poll(self, serial, ser_n):
        self.poll[ser_n] = select.poll()
        self.poll[ser_n].register(serial, select.POLLIN)

    def log_for(device, secs):
        global pyb
        end = time.time() + secs
        while time.time() < end:
            events = poll.poll(1000)
            for file in events:
                if file[0] == pyb[device].serial.fileno():
                    ch = pyb[device].serial.read(1)
                    print(ch.decode("utf-8"), end="")

    # class MailMan():

    # def __init__(self, device, baud=115200, timeout=1):
    #     self.serial = serial.Serial(device, baud, timeout=timeout)

    # def receive(self, ser_n) -> str:
    #     line = self.pyb[ser_n].read_until(self.TERMINATOR)
    #     return line.decode('utf-8').strip()

    # def send(self, ser_n, text: str) -> bool:
    #     line = '%s\r\f' % text
    #     self.pyb[ser_n].serial.write(line.encode('utf8'))
    #     # the line should be echoed.
    #     # If it isn't, something is wrong.
    #     return text == self.receive()

    # def write(self, string):
    #     self.serial.write(string)

    # def is_open(self):
    #     print(self.serial.is_open)

    # def close(self):
    #     self.serial.close()

    def run(self):
        self.window_serial.mainloop()


labels = create_labels()
win = SerialWindow(labels, [200, 100, 100, 100])
win.run()
