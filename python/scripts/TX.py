import serial
import dPyMR
import time

radioSerial = serial.Serial('/dev/tty.usbserial-145230', 9600, timeout = 2)

ownID = 1107
otherID = 1748
msg = 'This is a test ! :D'

radio = dPyMR.Transceiver(radioSerial, ownID)

print(radio.sendStatus(1, otherID, verbose = True))

msgSent = False
while msgSent == False:
  if radio.sendMessage(msg, otherID, verbose = True) == 'ACK_OK':
    print('ACK_OK')
    msgSent = True
  time.sleep(2)

while(True):
  inCmd = radio.receiveCommand(10)
  if inCmd == 'TIMEOUT_ERROR':
    print('TIMEOUT_ERROR')
  else :
    print('<- {}'.format(inCmd))