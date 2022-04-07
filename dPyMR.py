import time
import serial

class Transceiver :
  def __init__(self, dPyMRserial, ownID, MSGCH = -1, DEFCH = -1, timeout = 2):
    self.dPyMRserial = dPyMRserial
    self.ownID = ownID
    self.timeout = timeout
    self.ownID = ownID

    self.bol = b'\x02'
    self.eol = b'\x03'

    if MSGCH == -1 :
      self.MSGCH = self.getChannel()
    else :
      self.MSGCH = MSGCH
    
    if DEFCH == -1 :
      self.DEFCH = self.getChannel()
    else :
      self.DEFCH = DEFCH

    self.setChannel(self.DEFCH)

  def discover(self, idRange = (0, 9999999)) :
    # TODO: Implement this function
    return ()

  def sendCommand(self, command):
    data = self.bol + command.encode("utf-8") + self.eol
    self.dPyMRserial.write(data)

  def sendMessage(self, message, otherID):
    self.setChannel(self.MSGCH, resetDefault = True)

    command = '*SET,DPMR,TXMSG,IND,{},{},MSG,"{}",ACK'.format(str(otherID).zfill(7), str(self.ownID).zfill(7), message)
    self.sendCommand(command)
    
    response = b'' 
    byteread = b''
    beginTime = time.time()
    while not '*NTF,DPMR,TXMSG,IND,' in str(response.decode('utf-8')) :
      if(time.time() - beginTime > self.timeout):
        if(response == b''):
          self.setChannel(self.DEFCH)
          return 'TIMEOUT_ERROR'
      byteread = self.dPyMRserial.read() #Read one byte, stuff it in a temp variable
      response += byteread #Add it to the read string
    while not (byteread==self.eol): #While we haven't received eol
      byteread = self.dPyMRserial.read() #Read one byte, stuff it in a temp variable
      response += byteread #Add it to the read string

    if '"' + message + '",ACK,OK' in str(response.decode('utf-8')) :
      self.setChannel(self.DEFCH)
      return 'ACK_OK'
    elif '"' + message + '",ACK,NG' in str(response.decode('utf-8')) :
      self.setChannel(self.DEFCH)
      return 'ACK_NG'
    else :
      self.setChannel(self.DEFCH)
      return 'UNKNOWN_ERROR'

  def receiveCommand(self):
    # TODO : Implement this function
    return None

  def receiveMessage(self):
    # TODO : Implement this function
    return None

  def setChannel(self, channel, resetDefault = False):
    if resetDefault:
      self.DEFCH = self.getChannel()
    
    command = '*SET,MCH,SEL,{}'.format(str(channel))
    self.sendCommand(command)

  def getChannel(self, resetDefault = False):
    command = '*GET,MCH,SEL'
    self.sendCommand(command)
    response = b''
    byteread = b''
    beginTime = time.time()
    while not '*NTF,MCH,SEL,' in str(response.decode('utf-8')) :
      if(time.time() - beginTime > self.timeout):
        if(response == b''):
          return 'TIMEOUT_ERROR'
      byteread = self.dPyMRserial.read()
      response += byteread
    while not (byteread==self.eol):
      byteread = self.dPyMRserial.read()
      response += byteread
    currentChannel = int(response.decode('utf-8').split(',')[3][:-1])
    if resetDefault :
      self.DEFCH = currentChannel
    return currentChannel

  def setUItext(self, message = ""):
    command = '*SET,UI,TEXT,"{}"'.format(message)
    self.sendCommand(command)