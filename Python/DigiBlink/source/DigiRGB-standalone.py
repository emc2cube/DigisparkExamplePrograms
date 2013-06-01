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
# usbdevice arduino library already included, easier to use but won't reflect later changes on usbdevice library.
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

## Define ArduinoUsbDevice stuff (was in arduino/usbdevice.py
def getStringDescriptor(device, index):
    """
    """
    response = device.ctrl_transfer(usb.util.ENDPOINT_IN,
                                    usb.legacy.REQ_GET_DESCRIPTOR,
                                    (usb.util.DESC_TYPE_STRING << 8) | index,
                                    0, # language id
                                    255) # length

    # TODO: Refer to 'libusb_get_string_descriptor_ascii' for error handling
    
    return response[2:].tostring().decode('utf-16')

REQUEST_TYPE_SEND = usb.util.build_request_type(usb.util.CTRL_OUT,
                                                usb.util.CTRL_TYPE_CLASS,
                                                usb.util.CTRL_RECIPIENT_DEVICE)

REQUEST_TYPE_RECEIVE = usb.util.build_request_type(usb.util.CTRL_IN,
                                                usb.util.CTRL_TYPE_CLASS,
                                                usb.util.CTRL_RECIPIENT_DEVICE)

USBRQ_HID_GET_REPORT = 0x01
USBRQ_HID_SET_REPORT = 0x09
USB_HID_REPORT_TYPE_FEATURE = 0x03


class ArduinoUsbDevice(object):
    """
    """

    def __init__(self, idVendor, idProduct):
        """
        """
        self.idVendor = idVendor
        self.idProduct = idProduct

        # TODO: Make more compliant by checking serial number also.
        self.device = usb.core.find(idVendor=self.idVendor,
                                    idProduct=self.idProduct)

        if not self.device:
            raise Exception("Device not found")

    def write(self, byte):
        """
        """
        # TODO: Return bytes written?
        #print "Write:"+str(byte)
        self._transfer(REQUEST_TYPE_SEND, USBRQ_HID_SET_REPORT,
                       byte,
                       []) # ignored

    def read(self):
        """
        """
        response = self._transfer(REQUEST_TYPE_RECEIVE, USBRQ_HID_GET_REPORT,
                              0, # ignored
                              1) # length

        if not response:
            raise Exception("No Data")
        
        return response[0]

    def _transfer(self, request_type, request, index, value):
        """
        """
        return self.device.ctrl_transfer(request_type, request,
                                        (USB_HID_REPORT_TYPE_FEATURE << 8) | 0,
                                         index,
                                         value)

    @property
    def productName(self):
        """
        """
        return getStringDescriptor(self.device, self.device.iProduct)

    @property
    def manufacturer(self):
        """
        """
        return getStringDescriptor(self.device, self.device.iManufacturer)
## Done with definition

if __name__ == "__main__":

    theDevice = ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)

    print "Found: 0x%04x 0x%04x %s %s" % (theDevice.idVendor, 
                                          theDevice.idProduct,
                                          theDevice.productName,
                                          theDevice.manufacturer)

    import sys
    import time
    import webcolors

    if len(sys.argv)<3:

        color_list = webcolors.name_to_rgb(sys.argv[1].lower())
        color_list = list(color_list)
        color_list.insert(0, 0)
    else:
        color_list = sys.argv

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
