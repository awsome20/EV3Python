#!/usr/bin/env pybricks-micropython

# pybrick imports
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import wait, print

# there is only one tool we can use for interacting
# with the buttons, that's the brick's
# buttons() funciton which returns a list of the
# buttons pressed.

# What's a 'list'?  It's a new python data type 
# (like strings, ints, floats ...), but a little bit
# higher level.  A python list is a group of things
# that are all of the same data type.

# This is not a tutorial on lists.  Instead we'll just
# demonstrate some ways that the list of buttons 
# pressed can be used.

# in this example, we'll stay in a while loop
# forever and print the buttons pressed every second:
def testButtons():
    while True:
        pressed = brick.buttons()
        # 'len' is a special function that returns the length of a list
        numPressed = len(pressed)
        print("number of buttons pressed: ", numPressed)
        print("buttons pressed: ", pressed)
        if numPressed == 1:
            # Use the []'s to acces an element in the list
            # NOTE: zero is the FIRST element, not 1!!!!
            buttonPressed = pressed[0]
            if buttonPressed == Button.LEFT:
                print("You are pressing just the LEFT button!")
        wait(1000)

# call the function!
testButtons()        