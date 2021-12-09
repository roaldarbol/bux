import serial
from serial.tools import list_ports

class serial_connection():  

    def device(connection_type):
        s = None
        port = list(list_ports.comports())
        if len(port) > 0:
            for p in port:
                if connection_type in p.device:
                    print("Serial device:", p)
                    # Connection to port
                    s = serial.Serial(p.device)
                    print("Serial connected")
                    s.flush()
        else:
            s = None
            Warning("No ports")
        return(s)
    
    # def connect():
