import serial
from serial.tools import list_ports
import threading
from time import sleep

# working_serial = []
# for port in list(list_ports.comports()):
#     working_serial.append(port.device)
# print(working_serial)
serial_port = serial.Serial()

# GAP_DeviceInit  = \
#                 "\x01\x00\xfe\x26\x08\x03\x00\x00\x00\x00\x00\x00\x00\x00\
#                 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
#                 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00"

def read():
    while True:
        data = serial_port.read(9999);
        if len(data) > 0:
            print('Got:', data)

        sleep(0.5)
        print('not blocked')

def main():
    serial_port.baudrate = 115200
    serial_port.port = '/dev/cu.usbmodem142101'
    serial_port.timeout = 0
    if serial_port.isOpen(): serial_port.close()
    serial_port.open()
    t1 = threading.Thread(target=read, args=())
    while True:
        try:
            command = input('Enter a command to send to the Keyfob: \n\t')
            if (command != "stop"):
                serial_port.write(command)
        except KeyboardInterrupt:
            break

main()