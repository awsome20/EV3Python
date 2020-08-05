#!/usr/bin/env pybricks-micropython

# pybrick imports
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import wait, print

# The FLL mat is typically covered with lines which the robot can follow.
# It usually consists of a solid black line, about an inch thick, within
# a larger white line.

# 'line following' doesn't actually mean following a line, but rather
# following the border between two colors, black and white.
# this means the black and white lines form TWO lines to follow:
#   * black to the right, white to the left
#   * white to the right, black to the left

def lineFollow(blackOnRight):

    # make sure we got passed the right argument type
    assert isinstance(blackOnRight, bool)

    # setup the light sensor: TBF: make this a function argument
    lightPort = Port.S2
    lightSensor = ColorSensor(lightPort)

    # get these values by 'calibrating' the light sensor
    lightLow = 0.
    lightHigh = 100.

    # what is the value the sensor should be reading when it is
    # exactly above the white/black border?
    # here we'll use the non-calibrated version
    targetLight = lightLow + ((lightHigh - lightLow) / 2.0)

    # In all proporional programming, we need a 'gain' to convert
    # between our 'error' and how we correct for it.
    gain = 1.0

    # setup the motors
    leftMotor = Motor(Port.B)
    rightMotor = Motor(Port.C)

    # here we set the 'base' speed.  the actual power we set to
    # each motor will be determined by the light sensor
    # TBF: make this a function argument
    speed = 100

    # here, just drive forever
    # TBF: drive till we get to where we want to go
    while True:

        # get the reflected light intensity
        light = lightSensor.reflected()

        # how far off is this?
        error = light - targetLight

        # how do we correct for it?
        correction = error * gain

        # now we can apply this correction to the motor speeds, but
        # is this correction for turning to the left or right?
        # depends on which of the two lines we are following:
        if blackOnRight:
            leftTurnDir = 1.0 
            rightTurnDir = -1.0
        else:
            leftTurnDir = -1.0 
            rightTurnDir = 1.0

        # calculate the new power
        leftMotorPower = speed + (correction * leftTurnDir)
        rightMotorPower = speed + (correction * rightTurnDir)

        leftMotor.run(leftMotorPower)
        rightMotor.run(rightMotorPower)