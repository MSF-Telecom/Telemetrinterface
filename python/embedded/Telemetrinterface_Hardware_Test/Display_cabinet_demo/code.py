import time
import board
import rp2pio
import adafruit_pioasm
import neopixel
from rainbowio import colorwheel
import lib.dPyMR as dPyMR
import busio


pixel_pin = board.NEOPIXEL
buzzer_pin = board.BUZZ
num_pixels = 5


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False)

uart = busio.UART(board.TX0, board.RX0, baudrate=9600, timeout=2)
radio = dPyMR.Transceiver(uart, ownID, verbose=True)
parser = dPyMR.telemetrinterfaceFrameParser()

i2c = busio.I2C(board.SCL, board.SDA)  # SCL, SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

toggle = adafruit_pioasm.assemble(
    """
    set pins, 0
    set pins, 1
"""
)

# White stratup sequence with beeps
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

textSnippets = ["This is a demonstration",
                "of the Telemetrinterface",
                "That could be used",
                "to to gather data",
                "from a remote location",
                "or a car fleet",
                "or a weather station",
                "and store all of it",
                "on a centralized server",
                "to be integrated with",
                "other systems"]

while True:
  for snippet in textSnippets:
    radio.setUItext(snippet)
    rainbow_cycle(0.005)  # Increase the number to slow down the rainbow
  
  for _ in range(5):
    radio.setUItext("Telemetry demo !")
    color_chase((255, 0, 0), 0.1)
    color_chase((0, 255, 0), 0.1)
    color_chase((0, 0, 255), 0.1)
    radio.setUItext("Temp : " + str(bme280.temperature) + "°C")
    color_chase((255, 255, 0), 0.1)
    color_chase((0, 255, 255), 0.1)
    color_chase((255, 0, 255), 0.1)
    color_chase((255, 255, 255), 0.1)
    radio.setUItext("RH : " + str(bme280.relative_humidity) + "%")
    color_chase((0, 0, 0), 0.1)
  