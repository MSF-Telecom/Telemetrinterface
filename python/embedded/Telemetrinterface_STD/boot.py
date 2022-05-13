# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
import storage

usbsense = digitalio.DigitalInOut(board.USBSENSE)

usbsense.direction = digitalio.Direction.INPUT
usbsense.pull = digitalio.Pull.DOWN

# If the switch pin is connected to ground CircuitPython can write to the drive
USB_Connected = usbsense.value

debug = True

#storage.remount("/", (USB_Connected and debug == False))