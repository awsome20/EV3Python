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

# what's the min. speed that will cause the robot to move
minSpeed = 10

# make our motor objects
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)

# set them all to read zero
leftMotor.reset_angle(0)
rightMotor.reset_angle(0)

# read the left motor's current position
# this should just be zero.
angle = leftMotor.angle()

# start moving the robot straight - at our top speed!
leftMotor.run(speed)
rightMotor.run(speed)

# keep going until the left motor has rotated
# past our target angle
while angle < targetAngle:
    angle = leftMotor.angle()
    # how far have we gone?
    # we want this to be 1.0 at the start,
    # and then zero when angle == targetAngle (we get there)
    fractionComplete = 1.0 - (angle / targetAngle)
    # slow down according to how close we are
    rampSpeed = speed * fractionComplete
    # but down't slow down too much!
    rampSpeed = max(minSpeed, rampSpeed)
    # print how far we've come and how fast we're going
    print angle, rampSpeed
    leftMotor.run(rampSpeed)
    rightMotor.run(rampSpeed)

# now we can stop!
leftMotor.stop()
rightMotor.stop()
    