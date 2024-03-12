
# ICOM PC-CMD v2 Protocol info

A small list of usefull commands used in the dPyMR lib., reverse-engineered from an ICOM IC-F5061D radio. Other commands were guessed based on the logic of echoed commands (NTF)

## Commands

### Send message

```*SET,DPMR,TXMSG,IND,0000002,0000001,MSG,"This is a test",ACK```

### Get channel

```*GET,MCH,SEL```

### Set channel

```*SET,MCH,SEL,18```

### Set UI text

```*SET,UI,TEXT,"Noice"```

Return to default display:

```*SET,UI,TEXT,""```

### Press UI key

```*SET,UI,KEY,P3```

### Activate/Deactivate PTT

```*SET,UI,PTT,ON```
```*SET,UI,PTT,OFF```


### Send status number

```*SET,DPMR,TXSTAT,IND,0000002,0000001,1,ACK```

### Get Squelch status

```*GET,CTRL,SQL```

### Get Tx/Rx status

```*GET,CTRL,TX```

### Get own ID

> not found yet

### Set TX Power

> Not found yet

### Set GPS position and transmit it

> Not found yet
