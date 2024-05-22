
# ICOM PC-CMD v2 Protocol info

This document is a « Clean-Room” approach to reverse-engineering the CMD protocol used by ICOM Radios. This has been written with no access to internal ICOM tools nor documentation, only by analyzing the serial data out while interacting with the radios and additional control interfaces (+ educated guesses). 
Please note that depending on radio models and firmware versions, some commands might not be implemented.

## General layout
A PC-CMDV2 input line starts with an ASCII STX (0x02) and ends with an ASCII ETX (0x03). Its length can vary, depending on the command being sent. The parameters are comma-separated. Here’s a typical example:

```\0x02*NTF,CTRL,SQL,OPEN,5,-91\0x03```

Where: 
- ```\0X02``` is the START field
- ```*NTF``` is the HEAD field
- ```CTRL``` is the TYPE field, aka command type
- ```SQL,OPEN,5,-91``` is DATA-ARGS, data associate to the command
- ```\0x03``` is the END field

### HEAD fields
- ```*NTF```: always returned by the radio when getting a command result or a status
- ```*SET```: sent by the controller to set a specific setting, channel, status, trigger a message. It might or might not send a result
- ```*GET```: requests data from the radio: squelch status, internal settings, channel selection, etc. It always returns.

### TYPE fields
- CTRL: Related to general settings
- INFO: Related to general profile data
-	MCH: Related to channel control settings
-	UI: Related to user interface settings
-	DPMR: Related to dPMR-specific commands
-	IDAS: Related to IDAS (NXDN)-specific commands


## Commands

### Send message

```*SET,DPMR,TXMSG,IND,0000002,0000001,MSG,"This is a test",ACK```

### Get channel

```*GET,MCH,SEL```
**Returns**
```*NTF,MCH,SEL,1```

### Set channel

```*SET,MCH,SEL,18```
**If channel selection valid returns**
```*NTF,MCH,SEL,18```

**If channel selection invalid returns**
```*NTF,MCH,SEL,NG```



### Set UI text

```*SET,UI,TEXT,"Noice"```


Return to default display:

```*SET,UI,TEXT,""```

**No returns**

### Press UI key

```*SET,UI,KEY,P0```

**No returns**

### Activate/Deactivate PTT

```*SET,UI,PTT,[ON-OFF]```


### Send status number

```*SET,DPMR,TXSTAT,IND,0000002,0000001,1,ACK```

### Get Squelch status

```*GET,CTRL,SQL```

**If closed returns**
```*NTF,CTRL,SQL,CLOSE```

**If open returns**
```*NTF,CTRL,SQL,OPEN,+,RSSI```
Where RSSI is the signal strength

### Get profile comment lines

```*GET,INFO,COMMENT,1```
```*GET,INFO,COMMENT,2```

**Returns**
```*NTF,INFO,COMMENT,COMMENTCONTENTS ```
Where COMMENTCONTENTS is the profile's comment for each line

### Get Tx/Rx status

```*GET,CTRL,TX```

**If Tx disabled, returns**
```*NTF,CTRL,TX,OFF```

**If Tx enabled, returns**
```*NTF,CTRL,TX,ON```

### Get own ID

> not found yet

### Set TX Power

> Not found yet

### Set GPS position and transmit it

> Not found yet
