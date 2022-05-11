import time
import board
import busio
import adafruit_adxl34x
 
# Create sensor object, using the board's default I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)  # SCL, SDA
accelerometer = adafruit_adxl34x.ADXL345(i2c)
 
while True:
  print("%f %f %f" % accelerometer.acceleration)
  time.sleep(0.2)