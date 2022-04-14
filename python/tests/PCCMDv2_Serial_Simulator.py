import time

class RadioSerialSim :
  def __init__(self, port, baudrate, timeout = 2, verbose = False) :
    self.port = port
    self.baudrate = baudrate
    self.timeout = timeout
    self.verbose = verbose
    self.prevCMD = ''
    self.bol = b'\x02'
    self.eol = b'\x03'
    self.dataLen = 0
    self.dataIndex = -1
  
  def read(self, size) :
    # getChannel return string
    if '*GET,MCH,SEL' in self.prevCMD:
      retData = '*NTF,MCH,SEL,42'
      if self.verbose :
        print('<- {}'.format(retData))
      formatRetData = self.bol + retData.encode('utf-8') + self.eol
      unformatRetData = formatRetData.decode('utf-8')
      self.dataLen = len(formatRetData) 
      self.dataIndex +=1
      if(self.dataIndex >= self.dataLen):
        self.dataIndex = -1
        self.prevCMD = ''
        return b''
      if self.verbose:
        print('index : {}, len : {}, data :{}, retData : {}'.format(self.dataIndex, self.dataLen, unformatRetData[self.dataIndex], unformatRetData))
      return unformatRetData[self.dataIndex].encode('utf-8')
    # sendStatus return string
    elif '*SET,DPMR,TXSTAT,IND' in self.prevCMD :
      dataSplit = self.prevCMD.split(',')
      retData = '*NTF,DPMR,TXSTAT,IND,{},{},{},ACK,OK'.format(dataSplit[4], dataSplit[5], dataSplit[6])
      if self.verbose :
        print('<- {}'.format(retData))
      formatRetData = self.bol + retData.encode('utf-8') + self.eol
      unformatRetData = formatRetData.decode('utf-8')
      self.dataLen = len(formatRetData) 
      self.dataIndex +=1
      if(self.dataIndex >= self.dataLen):
        self.dataIndex = -1
        self.prevCMD = ''
        return b''
      if self.verbose:
        print('index : {}, len : {}, data :{}, retData : {}'.format(self.dataIndex, self.dataLen, unformatRetData[self.dataIndex], unformatRetData))
      return unformatRetData[self.dataIndex].encode('utf-8')
    # setChannel return string
    elif '*SET,MCH,SEL' in self.prevCMD :
      retData = '*NTF,MCH,SEL,42'
      if self.verbose :
        print('<- {}'.format(retData))
      formatRetData = self.bol + retData.encode('utf-8') + self.eol
      unformatRetData = formatRetData.decode('utf-8')
      self.dataLen = len(formatRetData) 
      self.dataIndex +=1
      if(self.dataIndex >= self.dataLen):
        self.dataIndex = -1
        self.prevCMD = ''
        return b''
      if self.verbose:
        print('index : {}, len : {}, data :{}, retData : {}'.format(self.dataIndex, self.dataLen, unformatRetData[self.dataIndex], unformatRetData))
      return unformatRetData[self.dataIndex].encode('utf-8')
    #sendMessage return string
    elif '*SET,DPMR,TXMSG,IND' in self.prevCMD :
      dataSplit = self.prevCMD.split(',')
      retData = '*NTF,DPMR,TXMSG,IND,{},{},MSG,{},ACK,OK'.format(dataSplit[4], dataSplit[5], dataSplit[7])
      if self.verbose :
        print('<- {}'.format(retData))
      formatRetData = self.bol + retData.encode('utf-8') + self.eol
      unformatRetData = formatRetData.decode('utf-8')
      self.dataLen = len(formatRetData) 
      self.dataIndex +=1
      if(self.dataIndex >= self.dataLen):
        self.dataIndex = -1
        self.prevCMD = ''
        return b''
      if self.verbose:
        print('index : {}, len : {}, data :{}, retData : {}'.format(self.dataIndex, self.dataLen, unformatRetData[self.dataIndex], unformatRetData))
      return unformatRetData[self.dataIndex].encode('utf-8')

    time.sleep(self.timeout)
    return b''

  def write(self, data) :
    self.dataIndex = -1
    self.prevCMD = data.decode('utf-8')
    if(self.verbose):
      print('-> {}'.format(data.decode("utf-8")))
    return len(data.decode("utf-8"))