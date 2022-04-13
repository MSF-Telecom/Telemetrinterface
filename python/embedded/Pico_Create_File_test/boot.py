# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.VBUS_SENSE)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.DOWN

# If the switch pin is connected to ground CircuitPython can write to the drive
USB_Connected = switch.value
storage.remount("/", USB_Connected)