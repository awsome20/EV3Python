#!/usr/bin/env pybricks-micropython

# pybrick imports
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# how far do we want to go?
targetAngle = 365

# how fast do we want to get there?
speed = 100

# make our motor objects
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)

# set them all to read zero
leftMotor.reset_angle(0)
rightMotor.reset_angle(0)

# read the left motor's current position
# this should just be zero.
angle = leftMotor.angle()

# start moving the robot straight
leftMotor.run(speed)
rightMotor.run(speed)

# keep going until the left motor has rotated
# past our target angle
while angle < targetAngle:
    angle = leftMotor.angle()
    # here we can change the speed!
    rampSpeed = speed
    leftMotor.run(rampSpeed)
    rightMotor.run(rampSpeed)

# now we can stop!
leftMotor.stop()
rightMotor.stop()
    