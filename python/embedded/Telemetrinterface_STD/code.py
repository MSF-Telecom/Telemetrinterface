import time
import board
import digitalio
import microcontroller
import storage
import lib.dPyMR as dPyMR
import busio
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_adxl34x

debug = True

usbsense = digitalio.DigitalInOut(board.USBSENSE)

usbsense.direction = digitalio.Direction.INPUT
usbsense.pull = digitalio.Pull.DOWN

prevSwitchValue = usbsense.value

if usbsense.value and debug == False:
  while True:
    led.value = True
    time.sleep(0.25)
    led.value = False
    time.sleep(0.25)
    if usbsense.value != prevSwitchValue:
      microcontroller.reset()

uart = busio.UART(board.GP16, board.GP17, baudrate=9600, timeout=2)

ownID = 1748
otherID = 1107
maxRetries = 5

radio = dPyMR.Transceiver(uart, ownID, verbose=True)

parser = dPyMR.telemetrinterfaceFrameParser()

nodeData = {"CPUTemp": [microcontroller.cpus[0].temperature, microcontroller.cpus[0].temperature],
            "CPUVolt": microcontroller.cpu.voltage, "Vers" : 1.0, "Reset" : microcontroller.cpu.reset_reason,
            "Push": False, "PushTime": 15,
            "temp": 21.5, "hum": 42, "press": 1023,
            "accel" : [9.81, 0.0, 0.0],
            "in1": False, "in2": False, "in3": False, "in4": False,
            "out1": False, "out2": False, "out3": False, "out4": False,
            "ain1": 12.6, "ain2": 4.7, "ain3": 24.2, "vsup": 13.8,
            "led1" : [34,198,0], "led2" : [12,0,230], "led3" : [44,27,102],
            "led4" : [0,44,128], "led5" : [243,14,95]}


i2c = busio.I2C(board.SCL, board.SDA)  # SCL, SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

accelerometer = adafruit_adxl34x.ADXL345(i2c)


def sendNodeData():
  nodeData = {"CPUTemp": [microcontroller.cpus[0].temperature, microcontroller.cpus[0].temperature],
            "CPUVolt": microcontroller.cpu.voltage, "Vers" : 1.0, "Reset" : microcontroller.cpu.reset_reason,
            "Push": False, "PushTime": 10,
            "temp": bme280.temperature, "hum": bme280.relative_humidity, "press": bme280.pressure,
            "accel" : accelerometer.acceleration,
            "in1": False, "in2": False, "in3": False, "in4": False,
            "out1": False, "out2": False, "out3": False, "out4": False,
            "ain1": 12.6, "ain2": 4.7, "ain3": 24.2, "vsup": 13.8,
            "led1" : [34,198,0], "led2" : [12,0,230], "led3" : [44,27,102],
            "led4" : [0,44,128], "led5" : [243,14,95]}

  msgs = ["", "", "", "", "", "", ""]

  SYSmsg = "$SYS,T,{},{},V,{},F,{},R,'{}'".format(
    nodeData["CPUTemp"][0],
    nodeData["CPUTemp"][1],
    nodeData["CPUVolt"],
    nodeData["Vers"],
    nodeData["Reset"],
  )
  msgs[0] = SYSmsg

  SETmsg = "$SET,P,{},I,{}".format(1 if nodeData["Push"] else 0, nodeData["PushTime"])
  msgs[1] = SETmsg

  ENVmsg = "$ENV,T,{},H,{},P,{},A,{},{},{}".format(
    nodeData["temp"],
    nodeData["hum"],
    nodeData["press"],
    nodeData["accel"][0],
    nodeData["accel"][1],
    nodeData["accel"][2],
  )
  msgs[2] = ENVmsg

  IOImsg = "$IOI,{},{},{},{}".format(
    1 if nodeData["in1"] else 0, 
    1 if nodeData["in2"] else 0,
    1 if nodeData["in3"] else 0,
    1 if nodeData["in4"] else 0
  )
  msgs[3] = IOImsg

  AINmsg = "$AIN,{},{},{},{}".format(
    nodeData["ain1"], nodeData["ain2"], nodeData["ain3"], nodeData["vsup"]
  )
  msgs[4] = AINmsg

  IOOmsg = "$IOO,{},{},{},{}".format(
    1 if nodeData["out1"] else 0, 
    1 if nodeData["out2"] else 0,
    1 if nodeData["out3"] else 0,
    1 if nodeData["out4"] else 0
  )
  msgs[5] = IOOmsg

  LEDmsg = "$LED,{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    nodeData["led1"][0], nodeData["led1"][1], nodeData["led1"][2],
    nodeData["led2"][0], nodeData["led2"][1], nodeData["led2"][2],
    nodeData["led3"][0], nodeData["led3"][1], nodeData["led3"][2],
    nodeData["led4"][0], nodeData["led4"][1], nodeData["led4"][2],
    nodeData["led5"][0], nodeData["led5"][1], nodeData["led5"][2],
  )
  msgs[6] = LEDmsg

  for msg in msgs:
    msgSent = False
    retries = 0
    while msgSent == False or retries == maxRetries:
      txStatus = radio.sendMessage(msg, otherID, verbose=True)
      retries += 1
      if txStatus == "ACK_OK":
        print("ACK_OK")
        msgSent = True
      else :
        print("TX_FAILED")
        time.sleep(2)


while True:
  
  if nodeData["Push"]:
    sendNodeData()

    timeNow = time.time()
    while time.time() - timeNow < nodeData["PushTime"]:
      inMSG = radio.receiveMessage()
      print(inMSG)
      if '$BUZ' in inMSG[2]:
        delay = float(inMSG[2].split(",")[1])
        if delay > 0:
          led.value = True
          time.sleep(delay/1000)
          led.value = False
  else :
    inMSG = radio.receiveMessage()
    print(inMSG)
    if '$' in inMSG[2]:
      data = parser.parseFrame(inMSG[2])
      print(data)
      if data[0] == "GET":
        # GET command, pulls data from the node
        sendNodeData()

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

      elif data[0] == "LED":
        # LED command, sets the node's LED values
        for key in data[1]:
          nodeData[key] = data[1][key]
      elif data[0] == "BUZ":
        # BUZ command, sets the node's buzzer values
        delay = float(data[1]["buzz"])
        if delay > 0:
          led.value = True
          time.sleep(delay/1000)
          led.value = False

      else :
        print(data)
