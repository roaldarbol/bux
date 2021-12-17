import serial
import time
import csv

# Find serial port on Mac with "ls -1 /dev/cu.usbmodem*" in Terminal
port = "/dev/cu.usbmodem141401" # Serial port of Pico (for me)
baud = 9600 # Pico runs at 9600 baud (I think)
fileName="pico-data.csv" # Name of the CSV file generated
ser = serial.Serial(port, baud, timeout=1)
ser.flush()
print("Connected to Pico port:" + port)
file = open(fileName, "a")
print("Created file")

samples = 10 #how many samples to collect
print_labels = True
line = 0 # Start at 0 because our header is 0 (not real data)
while line <= samples:
    data = ser.readline().decode('utf-8').rstrip()
    if print_labels:
        if line==0:
            print("Printing Column Headers")
        else:
            print("Reading " + str(line) + ": Temperature is " + data + ' deg')

    with open("pico-data.csv","a") as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerow([time.time(),data])
    
    line = line+1

print("Data collection complete!")
file.close()