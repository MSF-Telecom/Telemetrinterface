import serial
import dPyMR

radioSerial = serial.Serial('/dev/tty.usbserial-145230', 4800, timeout = 2)

ownID = 1107
otherID = 1748
msg = 'This is a test ! :D'

radio = dPyMR.Transceiver(radioSerial, ownID)

print(radio.sendMessage(msg, otherID))

while(True):
  print(radio.receiveCommand(10))