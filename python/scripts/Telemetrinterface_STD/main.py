import sys
sys.path.append('../')
import serial
import lib.dPyMR as dPyMR
import time

radioSerial = serial.Serial('/dev/tty.usbserial-145210', 9600, timeout = 2)

ownID = 1107
otherID = 1748
msg = 'This is a test ! :D'

radio = dPyMR.Transceiver(radioSerial, ownID)

def parseMsg(msg):
  response = msg

  # add elements of a list together in a string

  return (int(response.split(',')[5]), int(response.split(',')[5]), response.split(',MSG,"')[-1].split('"')[0])

while(True):
  inCmd = radio.receiveMessage()
  print('<- {}'.format(inCmd))


