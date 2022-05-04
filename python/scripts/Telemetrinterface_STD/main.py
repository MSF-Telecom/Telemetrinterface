import sys
sys.path.append('../')
import serial
import lib.dPyMR as dPyMR
import time
import requests

radioSerial = serial.Serial('/dev/tty.usbserial-145210', 9600, timeout = 2)

ownID = 1107
otherID = 1748
msg = 'This is a test ! :D'

radio = dPyMR.Transceiver(radioSerial, ownID)

def parseMsg(msg):
  response = msg

  # add elements of a list together in a string

  return (int(response.split(',')[5]), int(response.split(',')[5]), response.split(',MSG,"')[-1].split('"')[0])

teleData = {0:
            {"CPUTemp": [0, 0],
            "CPUVolt": 0, "Vers" : 0.0, "Reset" : '',
            "Push": False, "PushTime": 0,
            "temp": 0, "hum": 0, "press": 0,
            "accel" : [0.0, 0.0, 0.0],
            "in1": False, "in2": False, "in3": False, "in4": False,
            "out1": False, "out2": False, "out3": False, "out4": False,
            "ain1": 0, "ain2": 0, "ain3": 0, "vsup": 0,
            "led1" : [0,0,0], "led2" : [0,0,0], "led3" : [0,0,0],
            "led4" : [0,0,0], "led5" : [0,0,0]}
            }

while(True):
  inMessage = radio.receiveMessage()
  print('<- {}'.format(inMessage))
  if inMessage[2].startswith('$'):
    nodeID = inMessage[0]
    if inMessage not in teleData:
      teleData[nodeID] = {
            "CPUTemp": [0, 0],
            "CPUVolt": 0, "Vers" : 0.0, "Reset" : '',
            "Push": False, "PushTime": 0,
            "temp": 0, "hum": 0, "press": 0,
            "accel" : [0.0, 0.0, 0.0],
            "in1": False, "in2": False, "in3": False, "in4": False,
            "out1": False, "out2": False, "out3": False, "out4": False,
            "ain1": 0, "ain2": 0, "ain3": 0, "vsup": 0,
            "led1" : [0,0,0], "led2" : [0,0,0], "led3" : [0,0,0],
            "led4" : [0,0,0], "led5" : [0,0,0]}


    data = inMessage[2].split(',')
    if data[0] == '$SYS':
      teleData[nodeID]['CPUTemp'][0] = float(data[2])
      teleData[nodeID]['CPUTemp'][1] = float(data[3])
      teleData[nodeID]['CPUVolt'] = float(data[5])
      teleData[nodeID]['Vers'] = float(data[7])
      teleData[nodeID]['Reset'] = data[9]
    elif data[0] == '$SET':
      teleData[nodeID]['Push'] = True if data[2] == '1' else False
      teleData[nodeID]['PushTime'] = int(data[4])
    elif data[0] == '$ENV':
      teleData[nodeID]['temp'] = float(data[2])
      teleData[nodeID]['hum'] = float(data[4])
      teleData[nodeID]['press'] = float(data[6])
      teleData[nodeID]['accel'][0] = float(data[8])
      teleData[nodeID]['accel'][1] = float(data[9])
      teleData[nodeID]['accel'][2] = float(data[10])
    elif data[0] == '$IOI':
      teleData[nodeID]['in1'] = True if data[1] == '1' else False
      teleData[nodeID]['in2'] = True if data[2] == '1' else False
      teleData[nodeID]['in3'] = True if data[3] == '1' else False
      teleData[nodeID]['in4'] = True if data[4] == '1' else False
    elif data[0] == '$IOO':
      teleData[nodeID]['out1'] = True if data[1] == '1' else False
      teleData[nodeID]['out2'] = True if data[2] == '1' else False
      teleData[nodeID]['out3'] = True if data[3] == '1' else False
      teleData[nodeID]['out4'] = True if data[4] == '1' else False
    elif data[0] == '$AIN':
      teleData[nodeID]['ain1'] = float(data[1])
      teleData[nodeID]['ain2'] = float(data[2])
      teleData[nodeID]['ain3'] = float(data[3])
      teleData[nodeID]['vsup'] = float(data[4])
    elif data[0] == '$LED':
      teleData[nodeID]['led1'][0] = float(data[1])
      teleData[nodeID]['led1'][1] = float(data[2])
      teleData[nodeID]['led1'][2] = float(data[3])
      teleData[nodeID]['led2'][0] = float(data[4])
      teleData[nodeID]['led2'][1] = float(data[5])
      teleData[nodeID]['led2'][2] = float(data[6])
      teleData[nodeID]['led3'][0] = float(data[7])
      teleData[nodeID]['led3'][1] = float(data[8])
      teleData[nodeID]['led3'][2] = float(data[9])
      teleData[nodeID]['led4'][0] = float(data[10])
      teleData[nodeID]['led4'][1] = float(data[11])
      teleData[nodeID]['led4'][2] = float(data[12])
      teleData[nodeID]['led5'][0] = float(data[13])
      teleData[nodeID]['led5'][1] = float(data[14])
      teleData[nodeID]['led5'][2] = float(data[15])
    else:
      print('Unknown frame: {}'.format(data))

    r = requests.post('http://localhost:8080/control/data', json=teleData)
    print(r.status_code, r.reason)

  


