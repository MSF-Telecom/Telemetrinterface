# Telemetrinterface Data Transfer Protocol (TiDTP) Frame desctiption

## Frame Format

TiDTP frames consist of bytes (characters), and have a maximum length of 100 bytes. The first bite is a ```$```, followed by a word to describe the sent data type with a ```,``` after it. Then, the rest of the correspond to the data sent by a Telemetrinterface node.

## Frame Words

### ```$SYS```

System : System data such as core temperature, core voltage, firmware version and last reset reason.

> Sent from node to server

Example frame : ```$SYS,T,25.5,27.4,V,3.3,F,1.0,R,0```

### ```$SET```

Settings : Node settings such as Enable Push and Push interval (seconds).

> Sent from node to server to read settings, and from server to node to set settings.

Example frame : ```$SET,P,1,I,60```

### ```$ENV```

Environment : Environmental data such as temperature, humidity, pressure and acceleration from a node.

> Sent from node to server

Example frame : ```$ENV,T,25.5,H,50.5,P,1013.25,A,0.0,0.0,0.0```

### ```$IOI```

IO Inputs : State of the 4 digital inputs of a node.

> Sent from node to server

Example frame : ```$IOI,0,0,0,0```

### ```$ANI```

Analog Inputs : Voltage of the 4 analog inputs of a node. The 4th input is internally monitoring the supply voltage of the node.

> Sent from node to server

Example frame : ```$ANI,0.0,0.0,0.0,0.0```

### ```$IOO```

IO Outputs : State of the 4 digital outputs of a node.

> Sent from node to server to read the state, and from server to node to set the state

Example frame : ```$IOO,0,0,0,0```

### ```$LED```

LED State : Red, Green and Blue values of the 5 LEDs of a node.

> Sent from node to server to read the state, and from server to node to set the state

Example frame : ```$LED,255,0,0,0,255,0,0,0,255,255,255,255,0,0,0```

### ```$BUZ````

Buzzer State : Duration of a buzzer sound (miliseconds) to trigger on a node.

> Sent from server to node

Example frame : ```$BUZ,500```
