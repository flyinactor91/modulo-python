#!/usr/bin/python

import modulo, math


import random
#knob.setColor(random.random(),random.random(),random.random())

def knobTest() :
    port = modulo.Port()
    knob = modulo.Knob(port)
    knob.setHSV(random.random(),random.random(),random.random())

    def positionChanged(k) :
        k.setHSV(k.getAngle()/360.0, 1.0, 1.0)

    knob.positionChangeCallback = positionChanged

    port.runForever()

def joystickTest() :
    port = modulo.Port()
    joystick = modulo.Joystick(port)

    def positionChanged(j) :
        print j.getHPos(), j.getVPos(), j.getButton()

    def buttonPressed(j) :
        print 'press'

    def buttonReleased(j) :
        print 'release'

    joystick.buttonPressCallback = buttonPressed
    joystick.buttonReleaseCallback = buttonReleased
    joystick.positionChangeCallback = positionChanged
    print "address: ", joystick.getAddress()
    print "id: ", joystick.getDeviceID()

    port.runForever()

knobTest()


# # Open the first Modulo Controller serial port
# port = modulo.SerialPort()

# knob = port.get_knob()
# #knob.setColor(255,255,255)

# dpad = port.get_dpad()

# thermocouple = port.get_thermocouple()

# clock = port.get_clock()

# display = port.get_mini_display()

# previousPosition = None

# while (1) :
#     #print 'Finding Devices'
#     #deviceID = moduloBus.get_next_device_id(0)
#     #while deviceID is not None :
#     #    print hex(deviceID), moduloBus.get_address(deviceID), moduloBus.get_device_type(deviceID)
#     #    deviceID = moduloBus.get_next_device_id(deviceID+1)
#     #import time
#     #time.sleep(.1)
#     #print thermocouple.getTemperatureF(), dpad.getButton(0), dpad.getButton(1), knob.getButton(), knob.getPosition()

#     newPosition = knob.get_position()
#     if (previousPosition == newPosition) :
#         import time
#         time.sleep(.05)
#     else :
#         previousPosition = newPosition
#         angle = (newPosition % 24)*2*math.pi/24

#         display.clear()
#         display.draw_pixel(10,10, True)
#         display.draw_line([display.get_width()/2,display.get_height()/2,
#                 display.get_width()/2 + 20*math.cos(angle),
#                 display.get_height()/2 + 20*math.sin(angle)])
#         display.draw_rectangle(20,20,10,10)
#         display.update()

#         knob.set_color(255,255,0)
