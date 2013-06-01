#!/usr/bin/env python2

#
# Written for PyUSB 1.0 (w/libusb 1.0.3)
#
# Includes functionality to retrieve string descriptors
#
# Author: follower@rancidbacon.com
#
# Version: 20091021
#

##
# Modifications for Archlinux ARM platform. Should probably run with non-ARM Archlinux distributions.
#
# Author: emc2cube
# Git repository https://github.com/emc2cube/DigisparkExamplePrograms
#
# Install:
#
# You must have python2, pip, libusb and webcolors:
# sudo pacman -Sy python2 python2-pip
# sudo pip-2.7 install webcolors pyusb
#
# Optional:
#
# To be able to control the RGB LED as non-root user add this to your UDEV rules and reboot.
# echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"16c0\", ATTR{idProduct}==\"05df\", MODE:=\"0666\"" | sudo tee /etc/udev/rules.d/85-digispark.rules
#
#
# Assumes 'DigiBlink' is loaded on the board (from DigiArduino app -> Samples -> DigisparkUSB -> DigiBlink) and 
# LEDs are present on pins 11, 12 and 13 (default for RGBShield)
##

import usb # 1.0 not 0.4


import sys
sys.path.append("..")

from arduino.usbdevice import ArduinoUsbDevice


if __name__ == "__main__":

    theDevice = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)

    print "Found: 0x%04x 0x%04x %s %s" % (theDevice.idVendor, 
                                          theDevice.idProduct,
                                          theDevice.productName,
                                          theDevice.manufacturer)

    import sys
    import time
    import webcolors

    #sequence = [11,12,13]* 20
    #random.shuffle(sequence)

    #print "Look over there, flashing lights!"

    if len(sys.argv)<3:

        color_list = webcolors.name_to_rgb(sys.argv[1].lower())
        color_list = list(color_list)
        color_list.insert(0, 0)
    else:
        color_list = sys.argv

   # while 1:
        #pin = int(pin)

        #if output == "\r":
        #    print line
        #    line =""
        #else:
        #    line += output
        #else:

        #    print "Pin response didn't match."

    #byte val = sys.argv[1]
    print color_list

    theDevice.write(ord("s"))

    if color_list[1] == 0:
        theDevice.write(0)
    else:
        theDevice.write(int(color_list[1]))

    if color_list[2] == 0:
        theDevice.write(0)
    else:
        theDevice.write(int(color_list[2]))

    if color_list[3] == 0:
        theDevice.write(0)
    else:
        theDevice.write(int(color_list[3]))

    #theDevice.write(ord("e"))
        #time.sleep(2)

    #print
