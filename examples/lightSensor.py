#!/usr/bin/env pybricks-micropython

# pybrick imports
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import wait, print


def displayColorValues(port):
    "Continously prints color values at given port"
    print("displayColorValues")
    # creat the sensor object from the ColorSensor class
    sensor = ColorSensor(port)
    i = 0
    while True:
        # have four different ways of using this
        # sensor!
        color = sensor.color()
        print(i)
        i += 1
        # Color.BLACK, Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED, Color.WHITE, Color.BROWN or None
        if color == Color.BLACK:
            c = "Black"
        elif color == Color.BLUE:
            c = "Blue"
        elif color == Color.GREEN:
            c = "Green"
        elif color == Color.YELLOW:
            c = "Yellow"
        elif color == Color.RED:
            c = "Red"
        elif color == Color.WHITE:
            c = "White"
        else:
            c = "Unknown"
        print("color = ", c)                            
        wait(1000)

def displayLightValue(port):
    "Continously prints all values from color sensor at given port"

    # creat the sensor object from the ColorSensor class
    sensor = ColorSensor(port)

    while True:
        # have four different ways of using this
        # sensor!
        color = sensor.color()
        reflection = sensor.reflection()
        ambient = sensor.ambient()
        rgb = sensor.rgb()
        print("color: ", color)
        print("reflection: ", reflection)
        print("ambient: ", ambient)
        print("rgb: ", rgb)
        wait(1000)

def printMsg(msg):
    print(msg)
    brick.display.text(msg)

def getSensorValue(sensor):
    return sensor.reflection()
    # return sensor.ambient()

def calibrateLightSensor(port):
    sensor = ColorSensor(port)
    
    # first display values
    btns = brick.buttons()
    while len(btns) == 0:
        r = getSensorValue(sensor)
        printMsg("value on port %d: %f" % (port, r))
        printMsg("press any key")
        wait(10)
        btns = brick.buttons()

    
    printMsg("place over dark, then press any key")
    wait(2000)
    btns = brick.buttons()
    while len(btns) == 0:
        r = getSensorValue(sensor)
        btns = brick.buttons()

    low = r
    printMsg("dark value is %f " % low)
    printMsg("light, press any key")
    wait(2000)
    btns = brick.buttons()
     
    while len(btns) == 0:
        r = getSensorValue(sensor)
        btns = brick.buttons()

    high = r
    printMsg("highest value: %f" % high)
    
    printMsg("calibrated values:")
    wait(2000)
    btns = brick.buttons()
    while len(btns) == 0:
        r = getSensorValue(sensor)
        c = calibrateValue(r, low, high)
        btns = brick.buttons()
        printMsg("calibrated value: %f " % c)
        wait(100)
    
    return low, high

def calibrateValue(value, low, high):
    height = high - low
    if height == 0:
        return 0.

    cal = (value / height) * 100.0
    cal = max(0., cal)
    cal = min(cal, 100.)

    return cal
    
# display the light values in Port #2
#port = Port.S2
#displayLightValue(port)