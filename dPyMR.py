import time

def sendMessage(_serOBJ, _message, _otherID, _ownID, timeout = 2):
  beginTime = time.time()
  bol = b'\x02'
  command = '*SET,DPMR,TXMSG,IND,'
  eol = b'\x03'
  data = bol + command.encode('utf-8') + str(_otherID).zfill(7).encode('utf-8') + ','.encode('utf-8') + str(_ownID).zfill(7).encode('utf-8') + ',MSG,"'.encode('utf-8') + _message.encode('utf-8') + '",ACK'.encode('utf-8') + eol
  _serOBJ.write(data)
  response = b'' 
  byteread = b''
  while not '*NTF,DPMR,TXMSG,IND,' in str(response.decode('utf-8')) :
    if(time.time() - beginTime > timeout):
      if(response == b''):
        return 'TIMEOUT_ERROR'
    byteread = _serOBJ.read() #Read one byte, stuff it in a temp variable
    response += byteread #Add it to the read string
  while not (byteread==eol): #While we haven't received eol
    byteread = _serOBJ.read() #Read one byte, stuff it in a temp variable
    response += byteread #Add it to the read string

  if '"' + _message + '",ACK,OK' in str(response.decode('utf-8')) :
    return 'ACK_OK'
  elif '"' + _message + '",ACK,NG' in str(response.decode('utf-8')) :
    return 'ACK_NG'
  else :
    return 'UNKNOWN_ERROR'