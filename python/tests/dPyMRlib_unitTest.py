import sys
sys.path.append('../')
import unittest
import lib.dPyMR as dPyMR
import PCCMDv2_Serial_Simulator as SerSim

radioSerial = SerSim.RadioSerialSim('/dev/tty.usbserial-145230', 9600, timeout = 2)

ownID = 0
otherID = 1

msg = 'This is a Unit Test'

radio = dPyMR.Transceiver(radioSerial, ownID)

class Test_dPyMR_lib(unittest.TestCase):
  def test_getChannel(self):
    print('test_getChannel')
    self.assertEqual(radio.getChannel(), 42)
  
  def test_setChannel(self):
    print('test_setChannel')
    self.assertEqual(radio.setChannel(42), 'OK')

  def test_sendStatus(self):
    print('test_sendStatus')
    self.assertEqual(radio.sendStatus(1, otherID, timeout=4), 'ACK_OK')

  def test_sendMessage(self):
    print('test_sendMessage')
    self.assertEqual(radio.sendMessage(msg, otherID, timeout=1), 'ACK_OK')
  
  def test_receiveCommand(self):
    print('test_receiveCommand')
    self.assertEqual(radio.receiveCommand(timeout = 1), 'TIMEOUT_ERROR')

  def test_receivevMessage(self):
    print('test_receivevMessage')
    self.assertEqual(radio.receiveMessage(timeout=1), (None, None, 'TIMEOUT_ERROR'))
  
  def test_zfill(self):
    print('test_zfill')
    self.assertEqual(radio.zfill('42', 7), '0000042')

if __name__ == '__main__':
  unittest.main()