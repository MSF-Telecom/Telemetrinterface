import time
import serial

class Transceiver :
  def __init__(self, dPyMRserial, ownID, MSGCH = -1, DEFCH = -1, timeout = 2):
    """
    Parameters :
    • dPyMRserial [serial] : The serial object of the transceiver
    • ownID [int] : The ID of the transceiver
    • MSGCH [int] : The channel to use for sending messages, defaults to current set channel
    • DEFCH [int] : The channel to use for receiving messages, defaults to current set channel
    • timeout [int] : The global timeout in seconds, defaults to 2
    """
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
    """
    • TODO : Implement this method
    """
    # TODO: Implement this function
    return ()

  def sendCommand(self, command):
    """
    Parameters :
    • command [string] : The command to send to the radio
    Returns :
    • Nothing
    """
    data = self.bol + command.encode("utf-8") + self.eol
    self.dPyMRserial.write(data)

  def sendMessage(self, message, otherID, timeout = 10, verbose = False):
    """
    Parameters :
    • message [string] : The message to send
    • otherID [int] : The ID of the receiver
    • timeout [int] : The timeout in seconds
    • verbose [bool] : If true, print the response of the radio while the message is being sent
    Returns :
    • ACK [string] : The response of the radio :
      ACK_OK if the message was sent, 
      ACK_NG if the message was not sent, TIMEOUT_ERROR if the timeout was reached,
      UNKNOWN_ERROR if an unknown error occured
    """
    self.setChannel(self.MSGCH, resetDefault = True)

    command = '*SET,DPMR,TXMSG,IND,{},{},MSG,"{}",ACK'.format(str(otherID).zfill(7), str(self.ownID).zfill(7), message)
    if verbose :
      print("-> " + command)
    self.sendCommand(command)

    response = ''
    while not '*NTF,DPMR,TXMSG,IND,' in response :
      response = self.receiveCommand(timeout)
      if verbose :
        print(response)
      if response == 'TIMEOUT_ERROR' :
        return response

    if '"' + message + '",ACK,OK' in response :
      self.setChannel(self.DEFCH)
      return 'ACK_OK'
    elif '"' + message + '",ACK,NG' in response :
      self.setChannel(self.DEFCH)
      return 'ACK_NG'
    else :
      self.setChannel(self.DEFCH)
      return 'UNKNOWN_ERROR'

  def sendStatus(self, status, otherID, timeout = 10, verbose = False):
    """
    Parameters :
    • status [int] : The status to send to the radio
    Returns :
    • ACK [string] : The response of the radio :
      ACK_OK if the status was sent,
      ACK_NG if the status was not sent,
      TIMEOUT_ERROR if the timeout was reached,
      UNKNOWN_ERROR if an unknown error occured
    """
    
    self.setChannel(self.MSGCH, resetDefault = True)

    # *SET,DPMR,TXSTAT,IND,0001107,0001748,1,ACK
    command = '*SET,DPMR,TXSTAT,IND,{},{},{},ACK'.format(str(otherID).zfill(7), str(self.ownID).zfill(7), status)
    if verbose :
      print("-> " + command)
    self.sendCommand(command)

    response = ''
    while '*NTF,DPMR,TXSTAT,IND,' not in response :
      response = self.receiveCommand(timeout)
      if verbose :
        print(response)
      if response == 'TIMEOUT_ERROR' :
        return response
    
    if '"' + str(status) + '",ACK,OK' in response :
      self.setChannel(self.DEFCH)
      return 'ACK_OK'
    elif '"' + str(status) + '",ACK,NG' in response :
      self.setChannel(self.DEFCH)
      return 'ACK_NG'
    else :
      self.setChannel(self.DEFCH)
      return 'UNKNOWN_ERROR'

  def receiveCommand(self, timeout = 2):
    """
    Parameters :
    • timeout [int] : The timeout in seconds
    Returns :
    • response [string] : The response of the radio
    """
    # TODO : Verify & test function
    response = b''
    byteread = b''
    beginTime = time.time()
    self.dPyMRserial.flush()
    while not (byteread==self.eol):
      if(time.time() - beginTime > timeout):
        return 'TIMEOUT_ERROR'
      byteread = self.dPyMRserial.read()
      response += byteread

    self.dPyMRserial.flush()

    return response.decode('utf-8')[1:-1]

  def receiveMessage(self, timeout = 2, verbose = False):
    """
    Parameters :
    • timeout [int] : The timeout in seconds
    • verbose [bool] : If true, print the response of the radio while the message is being received
    Returns :
    • message [tuple] : The received & parsed message with (senderID [int], RSSI [int], Message [string])
    """
    # TODO : Verify & test function
    response = ''
    
    beginTime = time.time()
    while not '*NTF,DPMR,RXMSG,IND,' in response :
      response = self.receiveCommand(timeout)
      if verbose :
        print(response)
      if(response == 'TIMEOUT_ERROR'):
        return (None, None, response)

    return (int(response.split(',')[-5]), int(response.split(',')[-3]), response.split(',')[-1][1:-1])

  def setChannel(self, channel, resetDefault = False):
    """
    Parameters :
    • channel [int] : The channel to set
    • resetDefault [bool] : If true, reset the default channel to the current set channel
    Returns :
    • Nothing
    """
    if resetDefault:
      self.DEFCH = self.getChannel()
    
    command = '*SET,MCH,SEL,{}'.format(str(channel))
    self.sendCommand(command)

  def getChannel(self, resetDefault = False):
    """
    Parameters :
    • resetDefault [bool] : If true, reset the default channel to the current set channel
    Returns :
    • channel [int] : The current channel
    """
    command = '*GET,MCH,SEL'
    self.sendCommand(command)
    response = ""
    while not '*NTF,MCH,SEL,' in response :
      response = self.receiveCommand(self.timeout)
      if(response == 'TIMEOUT_ERROR'):
        return -1

    currentChannel = int(response.split(',')[-1])
    if resetDefault :
      self.DEFCH = currentChannel
    return currentChannel

  def setUItext(self, message = ""):
    """
    Parameters :
    • message [string] : The message to display on the UI, if set to "" the UI will be cleared
    Returns :
    • Nothing
    """
    command = '*SET,UI,TEXT,"{}"'.format(message)
    self.sendCommand(command)

if __name__ == '__main__':
  help(Transceiver)