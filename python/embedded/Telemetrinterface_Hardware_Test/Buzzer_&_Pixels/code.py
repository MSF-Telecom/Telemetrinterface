import time
import board
import rp2pio
import adafruit_pioasm
import neopixel
from rainbowio import colorwheel

pixel_pin = board.NEOPIXEL
buzzer_pin = board.BUZZ
num_pixels = 5


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False)


toggle = adafruit_pioasm.assemble(
    """
    set pins, 0
    set pins, 1
"""
)

for i in range(0, 5):
  pixels[4-i]= (255, 255, 255)
  sm = rp2pio.StateMachine(
          toggle, frequency=2000, first_set_pin=buzzer_pin
      )
  pixels.show()
  time.sleep(0.1)
  sm.deinit()
  time.sleep(0.1)


def color_chase(color, wait):
  for i in range(num_pixels):
    pixels[i] = color
    time.sleep(wait)
    pixels.show()
  time.sleep(0.5)


def rainbow_cycle(wait):
  for j in range(255):
    for i in range(num_pixels):
      rc_index = (i * 256 // num_pixels) + j
      pixels[i] = colorwheel(rc_index & 255)
    pixels.show()
    time.sleep(wait)


while True:
  rainbow_cycle(0.005)  # Increase the number to slow down the rainbow