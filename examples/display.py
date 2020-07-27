# pybrick imports
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import wait, print

def testDisplay():

    # first clear the display
    brick.display.clear()

    # now write some text on the screen, on line at a time:
    brick.display.text("line one")
    brick.display.text("line two")
    brick.display.text("line three")

    # let these lines of text stay on the screen
    # for at least for a few seconds
    wait(5000)

    # clear the screen again
    brick.display.clear()

    # now print stuff in the middle of the screen
    screenWidth = 177
    screenHeight = 127
    # our text will start halfway throught the width and height,
    # but these can't be float's!  127/2 = 63.5
    # so we convert them to integer's using the int() function.
    x = int(screenWidth/2)
    y = int(screenHeight/2)
    brick.display.text("I start in the middle", (int(177/2), int(127/2)))
    # display it for a few seconds
    wait(5000)

    # have some fun: print a character, but make it
    # go across the screen
    y = 50
    # range() returns a list starting from 0 up the number you give it.
    xPositions = range(screenWidth)
    # this for loop will go through each element in the list returned by
    # range:
    for x in xPositions:
        print("Print * at position: ", x, y)
        brick.display.clear()
        brick.display.text("*", (x, y))
        wait(10)