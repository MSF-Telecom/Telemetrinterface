import serial


ser=serial.Serial('/dev/tty.usbserial-145230', 4800, timeout = 2)
eol = b'\x03'

while True:
    response = b'' 
    byteread = b'' 
    while not (byteread==eol): #While we haven't received eol
        byteread = ser.read() #Read one byte, stuff it in a temp variable
        response += byteread #Add it to the read string
    datain = str(response.decode('utf-8')) #Convert it  and copy everything into a string
    print(response)
