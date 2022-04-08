import serial
import dPyMR
import time

radioSerial = serial.Serial('/dev/tty.usbserial-145230', 9600, timeout = 2)

ownID = 1107
otherID = 1748
msg = 'This is a test ! :D'

radio = dPyMR.Transceiver(radioSerial, ownID)

msgSent = False
while msgSent == False:
  if radio.sendMessage(msg, otherID, verbose = True) == 'ACK_OK':
    msgSent = True
  time.sleep(2)

while(True):
  print('<- {}'.format(radio.receiveCommand(10)))