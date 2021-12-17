from machine import Pin
import time

pin = Pin(25, Pin.OUT)
i = 0

while True:
    pin.toggle()
    time.sleep_ms(1000)
    i += 1
    print("hello", i)