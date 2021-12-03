import time
from drv8830 import DRV8830, I2C_ADDR1, I2C_ADDR2

motor = DRV8830(I2C_ADDR1)
motor.set_voltage(3)

t_on = 1
t_off = 29

while True:
    try:
        motor.reverse()
        time.sleep(t_on)
        motor.coast()
        time.sleep(t_off)
        motor.forward()
        time.sleep(t_on)
        motor.coast()
        time.sleep(t_off)
    except KeyboardInterrupt:
        print('Stopped script')