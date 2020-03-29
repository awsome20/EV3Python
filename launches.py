from pybricks.tools import print, wait
from pybricks import ev3brick as brick

def printMsg(msg):
    brick.display.text(msg)
    print(msg)

def launch1(robot):
    "Complete the missions for launch 1"

    brick.display.clear()

    printMsg("motors turned on")
    speed = 250.
    robot.start_drive_motors(speed)
    wait(1000)
    printMsg("motors turned off")
    robot.stop_drive_motors()