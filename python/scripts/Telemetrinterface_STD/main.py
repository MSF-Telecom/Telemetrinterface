import sys
from termios import tcdrain
sys.path.append('../')
import serial
import lib.dPyMR as dPyMR
import time
import requests
from flask import Flask, request
import threading
import json


radioSerial = serial.Serial('/dev/ttyUSB1', 9600, timeout = 2)

ownID = 6210
otherID = 4324
msg = 'This is a test ! :D'

radio = dPyMR.Transceiver(radioSerial, ownID)
txFlag = False
rxFlag = False

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

def transmitMessage(msg, ID):
  global radio
  global txFlag
  global rxFlag
  txFlag = True
  try :
    while rxFlag:
      print("waiting for radio")
      pass
    print("sending message")
    radio.sendMessage(msg, ID, verbose=True)
  except Exception as e:
    print(e)
  txFlag = False

app = Flask(__name__)

def radioHandler():
  while(True):
    global teleData
    global radio
    inMessage = []
    global txFlag
    global rxFlag
    if not txFlag:
      print("waiting for message")
      rxFlag = True
      inMessage = radio.receiveMessage()
      rxFlag = False
    #print('<- {}'.format(inMessage))

    if len(inMessage) > 0:
      if inMessage[2].startswith('$'):
        nodeID = inMessage[1]
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
            print(data[1][key])

        elif data[0] == 'AIN':
          for key in data[1]:
            teleData[nodeID][key] = data[1][key]

        elif data[0] == 'LED':
          for key in data[1]:
            teleData[nodeID][key] = data[1][key]

        else:
          print('Unknown frame: {}'.format(data))

        #r = requests.post('http://localhost:8080/control/data', json=teleData)
        #print(r.status_code, r.reason)



with app.app_context():
  def run_job():
    radioHandler()

  thread = threading.Thread(target=run_job)
  thread.start()

@app.route('/control/mode', methods=['POST'])
def setPollMode():
  data = json.loads(request.data.decode('utf-8'))
  print("Web interface updated mode")
  print(data)
  mode = 1 if data['mode'] == "push" else 0
  msg = '$SET,P,{},I,{}'.format(mode, 15)
  ID = int(data['nodeID'])

  transmitMessage(msg, ID)
  return 'OK'


@app.route('/control/outputs', methods=['POST'])
def setOutputs():
  data = json.loads(request.data.decode('utf-8'))
  print("Web interface updated outputs")
  print(data)
  msg = '$IOO,{},{},{},{}'.format(1 if data['outputs'][0] else 0, 1 if data['outputs'][1] else 0, 1 if data['outputs'][2] else 0, 1 if data['outputs'][3] else 0)
  ID = int(data['nodeID'])

  transmitMessage(msg, ID)
  return 'OK'

@app.route('/control/buzzer', methods=['POST'])
def result():
  print("Got data !!!!!")
  data = json.loads(request.data.decode("utf-8"))
  print(data)  # raw data

  msg = '$BUZ,{}'.format(int(data["buzzTime"]))
  ID = int(data['nodeID'])

  transmitMessage(msg, ID)
  
  return 'OK'

@app.route('/control/leds', methods=['POST'])
def leds():
  data = json.loads(request.data.decode("utf-8"))
  print(data)  # raw data

  msg = "$LED,{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
    data["RGB"][0], data["RGB"][1], data["RGB"][2],
    data["RGB"][3], data["RGB"][4], data["RGB"][5],
    data["RGB"][6], data["RGB"][7], data["RGB"][8],
    data["RGB"][9], data["RGB"][10], data["RGB"][11],
    data["RGB"][12], data["RGB"][13], data["RGB"][14]

  )
  ID = int(data['nodeID'])

  transmitMessage(msg, ID)

  return 'OK'


@app.route('/control/nodes', methods=['POST'])
def nodes():
  global teleData
  print("Web interface asked for nodes")
  return json.dumps(teleData)

@app.route('/', methods=['GET'])
def home():
  return 'Nothing to see here, just working in the background...'


if __name__ == "__main__":
  app.run(port=8081, debug=True, use_reloader=False, threaded=True)