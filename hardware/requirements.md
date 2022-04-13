# Telemetrinterface requirements

* **Power supply** :
  * **Voltage Input range** : 12-48V (VSUP)
  * **Current Input range** : TBD
  * Protected against reverse-polarity and over-voltage
* **Board voltage rails** :
  * **5V rail**
  * **3.3V rail**
  * **1.V rail** :
    * *Internal to RP2040 (no need for external regulator)*
  * Indicator lights and test pads on all voltage rails (except for 1.1V rail)
* **USB** :
  * Mini-USB connector
    * More robust, available
  * RP2040 aware of plugin-state
  * 5V Rail aware of plugin-state (Rail prefers VSUP if available)
  * Jumper for USB_HOST powering
* **Internal periferals** :
  * **Integrated LEDs** : 3
    * Independent or RGB ?
    * **Pins** :
      * GP25 (default ```board.LED``` pin on Pi Pico)
      * TBD
      * TBD
  * **Integrated Sensors** :
    * **BME280** (I2C or SPI) :
      * Pressure : 300hPa to 1100hPa, ±1.0hPa abs, ±0.12 rel
      * Temperature : -40°C to +85°C, 0°C-65°C full accuracy, ±0.5°C abs (at 25°C)
      * Humidity : 0% top 100%, ±3 %, ±2 % Hysteresis
    * **ADXL345** (I2C or SPI) :
      * Accelerometer : ±2g to ±16g, 3 axes, 13bit resolution
  * **Headers** :
    * All unused RP2040 GPIO pins are available for use on headers
* **External peripherals** :
  * **External GPIO** :
    * **Digital outputs** : 4 (8?)
      * Open-drain, active low
      * **MOSFETs** :
        * Voltage : 0-100V
        * Current : 0-5A
    * **Digital inputs** : 4 (8?)
      * Protected against reverse-polarity and over-voltage
      * Pull-up resistors (to VSUP rail) with cuttable traces on PCB
      * Buffered
    * **Analog inputs** : 2
      * Protected against reverse-polarity and over-voltage
      * 10MOhm input impedance
      * Resistor divider : 0-50V to 0-3.3V
      * Uses RP2040's internal ADC
  * **RS232/UART interface** :
    * RS232 and UARD port may need to be shared; this will be updated when the hardware is being designed.
    * **RS232** :
      * MAX232
      * Protected (need to find RS232 protection specs)
    * **UART** :
      * Buffered
      * Protecteds against reverse-polarity and over-voltage (TTL)
  * **I2C** :
    * Protected against over-voltage (TTL)
    * On-board pullup resistors (to 3.3V rail)
  * **SPI** :
    * Protected against over-voltage (TTL)
    * Buffered ?
  * **CAN** :
    * MCP2515 Controller (SPI interface; need to verify CircuitPythn lib availability)
    * MCP2551 Transceiver (need to verify compatibility with OBD port specs)
    * Protected (need to find CAN protection specs)
