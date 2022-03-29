import time
import serial
from serial.tools import list_ports

class serial_connection():
    def __init__(self, connection_type):
        self.connection_type = connection_type

    def connect_device(self):
        self.serial_device = None
        self.port = list(list_ports.comports())
        if len(self.port) > 0:
            for p in self.port:
                if self.connection_type in p.device:
                    print("Serial device:", p.device)
                    self.serial_device = serial.Serial(p.device, 115200, timeout=1)
                    if self.serial_device.is_open:
                        print("Serial connected")
                        self.serial_device.flush()
                    else:
                        "Serial connection failed"
        else:
            Warning("No ports")
        return(self.port)

    def read_serial(self):
        # data = self.serial_device.readline()#.decode('utf-8')#.rstrip()
        # ser_bytes = self.serial_device.readline()
        # data = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        data = self.serial_device.readline().decode('utf-8').rstrip()
        # bytesToRead = self.serial_device.inWaiting()
        # data = self.serial_device.read(bytesToRead)
        return(data)
    
    def close(self):
        self.serial_device.close()

# A bit for testing out:
# a = serial_connection(connection_type="usb")
# a.connect_device()
# i=0
# while i < 5:
#     print(a.read_serial())
#     i += 1
# a.close()

# ser = serial.Serial(
#     port='/dev/cu.usbmodem142201',
#     baudrate=115200
# )
# ser.write(b'hello')
# time.sleep(2)
# print(ser.read(10))
# ser.close()