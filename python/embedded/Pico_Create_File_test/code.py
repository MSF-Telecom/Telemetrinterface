import time
import board
import digitalio
import microcontroller
import storage

switch = digitalio.DigitalInOut(board.VBUS_SENSE)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.DOWN

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

prevSwitchValue = switch.value

if switch.value:
  while True:
    led.value = True
    time.sleep(0.25)
    led.value = False
    time.sleep(0.25)
    if(switch.value != prevSwitchValue):
      microcontroller.reset()

led.value = True
time.sleep(5)
with open("test.txt", "a") as f:
  f.write("Hello World!")
  f.flush()
time.sleep(1)
led.value = False
while(True):
  if(switch.value != prevSwitchValue):
    microcontroller.reset()