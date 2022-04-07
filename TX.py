import serial
from dPyMR import *

radio = serial.Serial('/dev/tty.usbserial-145230', 4800, timeout = 2)

ownID = 2
otherID = 1
msg = 'This is a test ! :D'

print(sendMessage(radio, msg, otherID, ownID))