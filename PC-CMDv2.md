
# ICOM PC-CMD v2 Protocol info

A small list of usefull commands used in the dPyMR lib., reverse-engineered from an ICOM IC-F5061D radio. Other commands were guessed based on the logic of echoed commands (NTF). 
Please note that depending on radio models and firmware versions, some commands might not be implemented.

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

```*SET,UI,PTT,ON```
```*SET,UI,PTT,OFF```


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
