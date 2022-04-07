import serial
from dPyMR import dPMR

radioSerial = serial.Serial('/dev/tty.usbserial-145230', 4800, timeout = 2)

ownID = 1107
otherID = 1748
msg = 'This is a test ! :D'

radio = dPMR(radioSerial, ownID)

print(radio.sendMessage(msg, otherID))