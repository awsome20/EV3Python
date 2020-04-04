from pybricks.tools import print, wait
from pybricks import ev3brick as brick

from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port

from robot import Robot

def printMsg(msg):
    brick.display.text(msg)
    print(msg)
    
def test_drive():

    r = Robot(debug=True)

    inches = 5.
    r.drive_straight_inches(200., inches)

    r.spin_left_to_angle(200., 90)
    r.spin_right_to_angle(400, -90)

def display_gyro_values():

    print("HW reset, then btn press:")
    while not any(brick.buttons()):
        wait(50)

    robot = Robot()
    wait(500)
    robot.reset_gyro_angle()
    wait(500)

    while True:
        angle = robot.get_gyro_angle()
        print(angle)
        wait(50)

def test_gyro_drift(port=Port.S4):

    gyro = GyroSensor(port)

    printMsg("Checking for drift.")
    numTests = 5
    drifting = False
    for i in range(numTests):
        angle = gyro.angle()
        printMsg("Test %i/%i = %d" % (i+1, numTests, angle))
        if angle != 0:
            drifting = True
            break # no need to keep testing
        wait(1000)

    return drifting

def prepare_gyro(port=Port.S4):
    """
    Run this before you use the gyro sensor to try and
    detect issues, and fix them.
    """

    drifting = True
    while drifting:
        drifting = test_gyro_drift(port=port)
        if drifting:
            printMsg("Detected Drift!")
            printMsg("Perform HW Cal,")
            printMsg("Then press any btn.")
            while not any(brick.buttons()):
                wait(50)
        else:
            printMsg("No Drift Detected.")    

    printMsg("Gyro ready for Use!")    