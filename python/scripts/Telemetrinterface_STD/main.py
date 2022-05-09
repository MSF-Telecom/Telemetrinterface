import sys
from termios import tcdrain
sys.path.append('../')
import serial
import lib.dPyMR as dPyMR
import time
import requests
from flask import Flask, request
from multiprocessing import Process, Value
import json


radioSerial = serial.Serial('/dev/tty.usbserial-145230', 9600, timeout = 2)

ownID = 1107
otherID = 1748
msg = 'This is a test ! :D'

radio = dPyMR.Transceiver(radioSerial, ownID)

parser = dPyMR.telemetrinterfaceFrameParser()

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


app = Flask(__name__)

@app.route('/control/data', methods=['POST'])
def result():
  print("Got data !!!!!")
  data = json.loads(request.data.decode("utf-8"))
  print(data)  # raw data
  radio.sendMessage('$BUZ,{}'.format(int(data["buzzTime"])), otherID, verbose=True)
  return 'OK'

@app.route('/', methods=['GET'])
def home():
  return 'Hello World!'

def radioHandler():
  while(True):
    inMessage = radio.receiveMessage()
    #print('<- {}'.format(inMessage))

    if inMessage[2].startswith('$'):
      nodeID = inMessage[0]
      msg = inMessage[2]
      data = parser.parseFrame(msg)
      if nodeID not in teleData:
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

      if data[0] == 'SYS':
        for key in data[1]:
          teleData[nodeID][key] = data[1][key]
  
      elif data[0] == 'SET':
        for key in data[1]:
          teleData[nodeID][key] = data[1][key]

      elif data[0] == 'ENV':
        for key in data[1]:
          teleData[nodeID][key] = data[1][key]

      elif data[0] == 'IOI':
        for key in data[1]:
          teleData[nodeID][key] = data[1][key]

      elif data[0] == 'IOO':
        for key in data[1]:
          teleData[nodeID][key] = data[1][key]

      elif data[0] == 'AIN':
        for key in data[1]:
          teleData[nodeID][key] = data[1][key]

      elif data[0] == 'LED':
        for key in data[1]:
          teleData[nodeID][key] = data[1][key]

      else:
        print('Unknown frame: {}'.format(data))

      r = requests.post('http://localhost:8080/control/data', json=teleData)
      #print(r.status_code, r.reason)



if __name__ == "__main__":
  recording_on = Value('b', True)
  p = Process(target=radioHandler)
  p.start()  
  app.run(port=8081, debug=True, use_reloader=False)
  p.join()