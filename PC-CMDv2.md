
# ICOM PC-CMD v2 Protocol - Introduction
This document is a « Clean-Room” approach to reverse-engineering the CMD protocol used by ICOM Radios. This has been written with no access to internal ICOM tools nor documentation, only by analyzing the serial data out while interacting with the radios and additional control interfaces (+ hours of typing random commands to see a reaction on the radio). 
Please note that depending on radio models and firmware versions, some commands might not be implemented.

# Command layout
A PC-CMDV2 input line starts with an ASCII STX (0x02) and ends with an ASCII ETX (0x03). Its length can vary, depending on the command being sent. The parameters are comma-separated. Here’s a typical example:

```\0x02*NTF,CTRL,SQL,OPEN,5,-91\0x03```

Where: 
- ```\0X02``` is the START field
- ```*NTF``` is the HEAD field
- ```CTRL``` is the TYPE field, aka command type
- ```SQL,OPEN,5,-91``` is DATA-ARGS, data associate to the command
- ```\0x03``` is the END field

## HEAD fields
- ```*NTF```: always returned by the radio when getting a command result or a status
- ```*SET```: sent by the controller to set a specific setting, channel, status, trigger a message. It might or might not send a result
- ```*GET```: requests data from the radio: squelch status, internal settings, channel selection, etc. It always returns.

## TYPE fields
- ```CTRL```: Related to general settings
- ```INFO```: Related to general profile data
- ```MCH```: Related to channel control settings
- ```UI```: Related to user interface settings
- ```DPMR```: Related to dPMR-specific commands
- ```IDAS```: Related to IDAS (NXDN)-specific commands


# Commands

## General settings (CTRL)

### Get Squelch status
```*GET,CTRL,SQL```
If closed returns
```*NTF,CTRL,SQL,CLOSE```
If open returns
```*NTF,CTRL,SQL,OPEN,+,RSSI```
Where RSSI is the signal strength


### Get Tx/Rx status
```*GET,CTRL,TX```
If Tx disabled, returns
```*NTF,CTRL,TX,OFF```
If Tx enabled, returns
```*NTF,CTRL,TX,ON```

## General info (INFO)
### Get profile comment lines
```*GET,INFO,COMMENT,[LINENR]```
Where LINENR is the comment field number (1 or 2)

Returns
```*NTF,INFO,COMMENT,[COMMENTCONTENTS] ```
Where COMMENTCONTENTS is the profile's comment for each line

### Get Electronic Serial Number (ESN)
```*GET,INFO,ESN```
Returns:
```*NTF,INFO,ESN,[SERIALNO]```
Where [SERIALNO] is the ESN

### Get firmware revision number (REV)
```*GET,INFO,REV```
Returns:
```*NTF,INFO,REV,[FWVERSION],[CHECKSUM]```
Where FWVERSION is the firmware's version number, CHECKUM is the firmware's checksum



## Channel (MCH)


### Get channel number
```*GET,MCH,SEL```
Returns:
```*NTF,MCH,SEL,[CHANNELNR]```
Where CHANNELNR is the channel on which the radio is.

### Set channel
```*SET,MCH,SEL,[CHANNELNR]```
Where CHANNELNR is the channel order number.
If channel selection invalid returns:
```*NTF,MCH,SEL,NG```

### Get channel frequency
```*GET,MCH,FREQ```
Returns:
```*NTF,MCH,FREQ,[FREQTX],[FREQRX]```
Where FREQTX and FREQRX are in Hz. 

### Set channel frequency
```*SET,MCH,FREQ,[FREQTX],[FREQRX]```
Where FREQTX and FREQRX are in Hz. Please note this is temporary and will revert back to the profile's frequency once channel is changed.
No return.

### Get channel CTCSS
```*GET,MCH,CTONE```
Returns:
```*GET,MCH,CTONE,[CTONEVALUE]```
Where CTONEVALUE is either OFF or the CTCSS value.

### Get channel bandwidth
```*GET,MCH,WNM```
Returns:
```*NTF,MCH,WNM,[MODE]```
Where MODE is either "Wide" or "Narrow". 

### Set channel bandwidth
```*SET,MCH,WNM,[MODE]```
Where MODE is either "Wide" or "Narrow". 
No return.


### Get RF Power
```*GET,MCH,RFPWR```
Returns:
```*NTF,MCH,RFPWR,[PWR]```
Where PWR is either "LOW1", "LOW2" or "HIGH". 

### Set RF Power
```*SET,MCH,RFPWR,[PWR]```
Where PWR is either "LOW1", "LOW2" or "HIGH". 
No return.

## User interface (UI)

### Set UI text
```*SET,UI,TEXT,[TEXT]```
Where [TEXT] is the text you want to display. 12 chars per line.
Return to default display:
```*SET,UI,TEXT,""```
No return.

### Press key
```*SET,UI,KEY,[KEY]```
Where [KEY] is the name of the button to press
No return.

### Activate/Deactivate PTT
```*SET,UI,PTT,[ON-OFF]```

### Set volume
```*SET,UI,AFVOL,[VOLUME]```
Where volume is from 0-255
No return

### Get volume
```*GET,UI,AFVOL```
Returns:
```*NTF,UI,AFVOL,[VOLUME]```
Where volume is from 0-255

### Reset radio
```*SET,UI,RESET```
No return 

## dPMR digital radio (DPMR)

### Send status number
```*SET,DPMR,TXSTAT,IND,0000002,0000001,1,ACK```

### Send message
```*SET,DPMR,TXMSG,IND,0000002,0000001,MSG,"This is a test",ACK```

## NXDN digital radio (NXDN)

### Send status number
```*SET,IDAS,TXSTAT,IND,2,1,2,ACK```

### Send message
```*SET,IDAS,TXMSG,IND,2,1,MSG,"This is a test",ACK```

### Stun radio
```*SET,IDAS,TXSTUN,IND,1892```

### Set radio ID (needed to receive text messages)
```*SET,IDAS,SENDID,TG,9900,65519```

### Get own ID
```*GET,IDAS,SENDID,TG```

### Set GPS position and transmit it
> Not found yet

