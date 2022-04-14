# Hardware design considerations

* **ADC front-ends** :
  * At least 10MOhm input impedance
  * Resistor divider : 0-50V to 0-3.3V
  * Uses RP2040's internal ADC
  * Design :
    * 10MOhm-680kOhm resistor divider (52V to 3.31V, minimum of 12.6536mV input at 12bits)
    * 3.3V Zener diode as over-voltage clamp

* **GPIO Input front-end** :
  * Design :
    * 10kOhm Pull-up resistors (to VSUP rail) with cuttable traces on PCB
    * 300Ohm input resistor (before zener, before or after pullup ?)
    * Clamping diodes to GND & VSUP rails

* **GPIO Outputs** :
  * Design :
    * NCE6005AS MOSFET
    * 10kOhm pulldown resistor on gate
    * Flyback diode from source to drain
    * Clamping diodes to GND & VSUP rails ?

* **I2C, SPI, UART** :
  * Design :
    * TPDxEUSB30 TVS ICs for protection

* **RS232** :
  * Design :
    * MAX232
    * No further protection seems needed

* **CAN** :
  * Design :
    * MCP2551
    * No further protection seems needed
