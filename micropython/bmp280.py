import time
from machine import Pin
from breakout_bmp280 import BreakoutBMP280
from pimoroni_i2c import PimoroniI2C

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

pin = Pin(25, Pin.OUT)
i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
bmp = BreakoutBMP280(i2c)
i = 0

while 1 < 30:
    reading = bmp.read()
    print(str(reading[0]), str(reading[1]), sep = ",")
    time.sleep(0.2)
    i += 1
    if i % 4 == 0:
        pin.toggle()