import lib.dPyMR as dPyMR
import board
import busio
import time

uart = busio.UART(board.GP16, board.GP17, baudrate=9600, timeout=2)

ownID = 1748
otherID = 1107
msg = 'This is an embedded test ! :D'

radio = dPyMR.Transceiver(uart, ownID)

while True:
  msgSent = False
  while msgSent == False:
    if radio.sendMessage(msg, otherID, verbose=True) == 'ACK_OK':
      print('ACK_OK')
      msgSent = True
    time.sleep(2)

  time.sleep(5)