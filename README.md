# Telemetrinterface

[![Code Checkout](https://github.com/fred-corp/MSF_ICOM-Telemetrinterface/workflows/Code%20Checkout/badge.svg)](https://github.com/fred-corp/MSF_ICOM-Telemetrinterface/actions/workflows/checkout.yml)

## ICOM PC-CMD v2 Protocol info

A small list of usefull commands used in the dPyMR lib., reverse-engineered from IP2Air and an ICOM IC-F5061D radio.

### Send message

```*SET,DPMR,TXMSG,IND,0000002,0000001,MSG,"This is a test",ACK```

### Get channel

```*GET,MCH,SEL```

### Set channel

```*SET,MCH,SEL,18```

### Set UI text

```*SET,UI,TEXT,"Noice"```

### Press UI key

```*SET,UI,KEY,P3```

### Send status number

```*SET,DPMR,TXSTAT,IND,0000002,0000001,1,ACK```

### Get own ID

> not found yet

### Set TX Power

> Not found yet

### Set GPS position and transmit it

> Not found yet
