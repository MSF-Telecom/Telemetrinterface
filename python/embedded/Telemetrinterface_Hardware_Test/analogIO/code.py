import time
import board
from analogio import AnalogIn

analog_in = AnalogIn(board.VSUP)


def get_voltage(pin):
  return (pin.value*440)/65536


while True:
  print("Raw : {}, Converted : {}V".format(analog_in.value, get_voltage(analog_in)))
  time.sleep(0.1)