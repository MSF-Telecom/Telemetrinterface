import time
import board
import digitalio
import analogio
import microcontroller
import storage
import lib.dPyMR as dPyMR
import busio
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_adxl34x
import neopixel
from rainbowio import colorwheel
import rp2pio
import adafruit_pioasm

debug = True

usbsense = digitalio.DigitalInOut(board.USBSENSE)

usbsense.direction = digitalio.Direction.INPUT
usbsense.pull = digitalio.Pull.DOWN


uart = busio.UART(board.TX0, board.RX0, baudrate=9600, timeout=2)

ownID = 1748
otherID = 1107
maxRetries = 5

radio = dPyMR.Transceiver(uart, ownID, verbose=True)

parser = dPyMR.telemetrinterfaceFrameParser()

nodeData = {
  "CPUTemp": [
    microcontroller.cpus[0].temperature,
    microcontroller.cpus[0].temperature,
  ],
  "CPUVolt": microcontroller.cpu.voltage,
  "Vers": 1.0,
  "Reset": microcontroller.cpu.reset_reason,
  "Push": True,
  "PushTime": 15,
  "temp": 21.5,
  "hum": 42,
  "press": 1023,
  "accel": [9.81, 0.0, 0.0],
  "in1": False,
  "in2": False,
  "in3": False,
  "in4": False,
  "out1": False,
  "out2": False,
  "out3": False,
  "out4": False,
  "ain1": 12.6,
  "ain2": 4.7,
  "ain3": 24.2,
  "vsup": 13.8,
  "led1": [34, 198, 0],
  "led2": [12, 0, 230],
  "led3": [44, 27, 102],
  "led4": [0, 44, 128],
  "led5": [243, 14, 95],
}


i2c = busio.I2C(board.SCL, board.SDA)  # SCL, SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

accelerometer = adafruit_adxl34x.ADXL345(i2c)


IN_1 = digitalio.DigitalInOut(board.IN1)
IN_1.direction = digitalio.Direction.INPUT
IN_2 = digitalio.DigitalInOut(board.IN2)
IN_2.direction = digitalio.Direction.INPUT
IN_3 = digitalio.DigitalInOut(board.IN3)
IN_3.direction = digitalio.Direction.INPUT
IN_4 = digitalio.DigitalInOut(board.IN4)
IN_4.direction = digitalio.Direction.INPUT

AIN1 = analogio.AnalogIn(board.SENSE1)
AIN2 = analogio.AnalogIn(board.SENSE2)
AIN3 = analogio.AnalogIn(board.SENSE3)
VSUP = analogio.AnalogIn(board.VSUP)

out1 = digitalio.DigitalInOut(board.OUT1)
out1.direction = digitalio.Direction.OUTPUT
out2 = digitalio.DigitalInOut(board.OUT2)
out2.direction = digitalio.Direction.OUTPUT
out3 = digitalio.DigitalInOut(board.OUT3)
out3.direction = digitalio.Direction.OUTPUT
out4 = digitalio.DigitalInOut(board.OUT4)
out4.direction = digitalio.Direction.OUTPUT


pixel_pin = board.NEOPIXEL
num_pixels = 5

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False)


buzzer_pin = board.BUZZ
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

for i in range(0, 5):
  pixels[4-i]= (0, 0, 0)
pixels.show()

# TODO for v2.0 Hardware : change resistor value from 68k to 680k
def get_voltage(pin):
  return (pin.value * 440) / 65536


def sendNodeData(dataToSend="ALL"):

  nodeData = {
    "CPUTemp": [
      microcontroller.cpus[0].temperature,
      microcontroller.cpus[0].temperature,
    ],
    "CPUVolt": microcontroller.cpu.voltage,
    "Vers": 1.0,
    "Reset": microcontroller.cpu.reset_reason,
    "Push": True,
    "PushTime": 10,
    "temp": bme280.temperature,
    "hum": bme280.relative_humidity,
    "press": bme280.pressure,
    "accel": accelerometer.acceleration,
    "in1": IN_1.value,
    "in2": IN_2.value,
    "in3": IN_3.value,
    "in4": IN_4.value,
    "out1": out1.value,
    "out2": out2.value,
    "out3": out3.value,
    "out4": out4.value,
    "ain1": get_voltage(AIN1),
    "ain2": get_voltage(AIN2),
    "ain3": get_voltage(AIN3),
    "vsup": get_voltage(VSUP),
    "led1": pixels[4],
    "led2": pixels[3],
    "led3": pixels[2],
    "led4": pixels[1],
    "led5": pixels[0],
  }

  SYSmsg = "$SYS,T,{},{},V,{},F,{},R,'{}'".format(
    nodeData["CPUTemp"][0],
    nodeData["CPUTemp"][1],
    nodeData["CPUVolt"],
    nodeData["Vers"],
    nodeData["Reset"],
  )
  if(dataToSend == "ALL") or (dataToSend == "SYS"):
    txMessage(SYSmsg)

  SETmsg = "$SET,P,{},I,{}".format(1 if nodeData["Push"] else 0, nodeData["PushTime"])
  if(dataToSend == "ALL") or (dataToSend == "SET"):
    txMessage(SETmsg)

  ENVmsg = "$ENV,T,{},H,{},P,{},A,{},{},{}".format(
    nodeData["temp"],
    nodeData["hum"],
    nodeData["press"],
    nodeData["accel"][0],
    nodeData["accel"][1],
    nodeData["accel"][2],
  )
  if(dataToSend == "ALL") or (dataToSend == "ENV"):
    txMessage(ENVmsg)

  IOImsg = "$IOI,{},{},{},{}".format(
    1 if nodeData["in1"] else 0,
    1 if nodeData["in2"] else 0,
    1 if nodeData["in3"] else 0,
    1 if nodeData["in4"] else 0,
  )
  if(dataToSend == "ALL") or (dataToSend == "IOI"):
    txMessage(IOImsg)

  AINmsg = "$AIN,{},{},{},{}".format(
    nodeData["ain1"], nodeData["ain2"], nodeData["ain3"], nodeData["vsup"]
  )
  if(dataToSend == "ALL") or (dataToSend == "AIN"):
    txMessage(AINmsg)

  IOOmsg = "$IOO,{},{},{},{}".format(
    1 if nodeData["out1"] else 0,
    1 if nodeData["out2"] else 0,
    1 if nodeData["out3"] else 0,
    1 if nodeData["out4"] else 0,
  )
  if(dataToSend == "ALL") or (dataToSend == "IOO"):
    txMessage(IOOmsg)

  LEDmsg = "$LED,{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    nodeData["led1"][0],
    nodeData["led1"][1],
    nodeData["led1"][2],
    nodeData["led2"][0],
    nodeData["led2"][1],
    nodeData["led2"][2],
    nodeData["led3"][0],
    nodeData["led3"][1],
    nodeData["led3"][2],
    nodeData["led4"][0],
    nodeData["led4"][1],
    nodeData["led4"][2],
    nodeData["led5"][0],
    nodeData["led5"][1],
    nodeData["led5"][2],
  )
  txMessage(LEDmsg)

def txMessage(msg):
  msgSent = False
  retries = 0
  while msgSent == False or retries == maxRetries:
    txStatus = radio.sendMessage(msg, otherID, verbose=True)
    retries += 1
    if txStatus == "ACK_OK":
      print("ACK_OK")
      msgSent = True
    else:
      print("TX_FAILED")
      time.sleep(2)


def listenForCommand(inMSG):
  if '$' in inMSG[2]:
    data = parser.parseFrame(inMSG[2])
    print(data)
    if data[0] == "GET":
      # GET command, pulls data from the node
      sendNodeData()
    
    elif data[0] == "MOD":
      # Sets poll mode
      nodeData["Push"] = True if data[1]["push"] == "push" else False
      nodeData["PushTime"] = data[1]["pushTime"]

    elif data[0] == "SYS":
      # SYS command, sets the node's system values (CPU vand Reset values may be overwritten by the node)
      for key in data[1]:
        nodeData[key] = data[1][key]

    elif data[0] == "SET":
      # SET command, sets the node's push and push time
      for key in data[1]:
        nodeData[key] = data[1][key]

    elif data[0] == "ENV":
      # ENV command, sets the node's environmental values (may be overwritten by the node)
      for key in data[1]:
        nodeData[key] = data[1][key]

    elif data[0] == "IOI":
      # IOI command, sets the node's input values (may be overwritten by the node)
      for key in data[1]:
        nodeData[key] = data[1][key]

    elif data[0] == "AIN":
      # AIN command, sets the node's analog input values (may be overwritten by the node)
      for key in data[1]:
        nodeData[key] = data[1][key]

    elif data[0] == "IOO":
      # IOO command, sets the node's output values
      for key in data[1]:
        nodeData[key] = data[1][key]
      out1.value = nodeData["out1"]
      out2.value = nodeData["out2"]
      out3.value = nodeData["out3"]
      out4.value = nodeData["out4"]
      time.sleep(0.2)
      sendNodeData("IOO")

    elif data[0] == "LED":
      # LED command, sets the node's LED values
      for key in data[1]:
        nodeData[key] = data[1][key]
        print(data[1][key])
      pixels[4] = (nodeData["led1"][0], nodeData["led1"][1], nodeData["led1"][2])
      pixels[3] = (nodeData["led2"][0], nodeData["led2"][1], nodeData["led2"][2])
      pixels[2] = (nodeData["led3"][0], nodeData["led3"][1], nodeData["led3"][2])
      pixels[1] = (nodeData["led4"][0], nodeData["led4"][1], nodeData["led4"][2])
      pixels[0] = (nodeData["led5"][0], nodeData["led5"][1], nodeData["led5"][2])
      pixels.show()
      sendNodeData("LED")

    elif data[0] == "BUZ":
      # BUZ command, sets the node's buzzer values
      delay = float(data[1]["buzz"])
      if delay > 0:
        sm = rp2pio.StateMachine(
          toggle, frequency=2000, first_set_pin=buzzer_pin
        )
        time.sleep(delay/1000)
        sm.deinit()

    else:
      print(data)

while True:

  if nodeData["Push"]:
    sendNodeData()

    timeNow = time.time()
    while time.time() - timeNow < nodeData["PushTime"]:
      inMSG = radio.receiveMessage()
      print(inMSG)
      listenForCommand(inMSG)

  else:
    inMSG = radio.receiveMessage()
    print(inMSG)
    listenForCommand(inMSG)
